import collections

### a pure python implementation of the dict data structure
# follows the interface laid down by Benjamin mcduder


MINSIZE = 8             ### initial size of dict items
PERTURB_SHIFT = 5       ### used in open addressing probe, see below
dummy = "<dummy key>"   ### used in open addressing probe, see below (??)

### a discusison of the open addressing scheme from the python dict 
'''
Major subtleties ahead:  Most hash schemes depend on having a "good" hash
function, in the sense of simulating randomness.  Python doesn't:  its most
important hash functions (for strings and ints) are very regular in common
cases:

    >>> map(hash, (0, 1, 2, 3))
    [0, 1, 2, 3]
    >>> map(hash, ("namea", "nameb", "namec", "named"))
    [-1658398457, -1658398460, -1658398459, -1658398462]
    >>>

This isn't necessarily bad!  To the contrary, in a table of size 2**i, taking
the low-order i bits as the initial table index is extremely fast, and there
are no collisions at all for dicts indexed by a contiguous range of ints.
The same is approximately true when keys are "consecutive" strings.  So this
gives better-than-random behavior in common cases, and that's very desirable.

OTOH, when collisions occur, the tendency to fill contiguous slices of the
hash table makes a good collision resolution strategy crucial.  Taking only
the last i bits of the hash code is also vulnerable:  for example, consider
the list [i << 16 for i in range(20000)] as a set of keys.  Since ints are
their own hash codes, and this fits in a dict of size 2**15, the last 15 bits
    of every hash code are all 0:  they *all* map to the same table index.

But catering to unusual cases should not slow the usual ones, so we just take
the last i bits anyway.  It's up to collision resolution to do the rest.  If
we *usually* find the key we're looking for on the first try (and, it turns
out, we usually do -- the table load factor is kept under 2/3, so the odds
are solidly in our favor), then it makes best sense to keep the initial index
computation dirt cheap.

The first half of collision resolution is to visit table indices via this
recurrence:

    j = ((5*j) + 1) mod 2**i

For any initial j in range(2**i), repeating that 2**i times generates each
int in range(2**i) exactly once (see any text on random-number generation for
proof).  By itself, this doesn't help much:  like linear probing (setting
j += 1, or j -= 1, on each loop trip), it scans the table entries in a fixed
order.  This would be bad, except that's not the only thing we do, and it's
actually *good* in the common cases where hash keys are consecutive.  In an
example that's really too small to make this entirely clear, for a table of
size 2**3 the order of indices is:

    0 -> 1 -> 6 -> 7 -> 4 -> 5 -> 2 -> 3 -> 0 [and here it's repeating]

If two things come in at index 5, the first place we look after is index 2,
not 6, so if another comes in at index 6 the collision at 5 didn't hurt it.
Linear probing is deadly in this case because there the fixed probe order
is the *same* as the order consecutive keys are likely to arrive.  But it's
extremely unlikely hash codes will follow a 5*j+1 recurrence by accident,
and certain that consecutive hash codes do not.

The other half of the strategy is to get the other bits of the hash code
into play.  This is done by initializing a (unsigned) vrbl "perturb" to the
full hash code, and changing the recurrence to:

j = (5*j) + 1 + perturb;
perturb >>= PERTURB_SHIFT;
use j % 2**i as the next table index;

Now the probe sequence depends (eventually) on every bit in the hash code,
and the pseudo-scrambling property of recurring on 5*j+1 is more valuable,
because it quickly magnifies small differences in the bits that didn't affect
the initial index.  Note that because perturb is unsigned, if the recurrence
is executed often enough perturb eventually becomes and remains 0.  At that
point (very rarely reached) the recurrence is on (just) 5*j+1 again, and
that's certain to find an empty slot eventually (since it generates every int
in range(2**i), and we make sure there's always at least one empty slot).

Selecting a good value for PERTURB_SHIFT is a balancing act.  You want it
small so that the high bits of the hash code continue to affect the probe
sequence across iterations; but you want it large so that in really bad cases
the high-order hash bits have an effect on early iterations.  5 was "the
best" in minimizing total collisions across experiments Tim Peters ran (on
both normal and pathological cases), but 4 and 6 weren't significantly worse.

Historical: Reimer Behrends contributed the idea of using a polynomial-based
approach, using repeated multiplication by x in GF(2**n) where an irreducible
polynomial for each table size was chosen such that x was a primitive root.
Christian Tismer later extended that to use division by x instead, as an
efficient way to get the high bits of the hash code into play.  This scheme
also gave excellent collision statistics, but was more expensive:  two
if-tests were required inside the loop; computing "the next" index took about
the same number of operations but without as much potential parallelism
(e.g., computing 5*j can go on at the same time as computing 1+perturb in the
above, and then shifting perturb can be done while the table index is being
masked); and the PyDictObject struct required a member to hold the table's
polynomial.  In Tim's experiments the current scheme ran faster, produced
equally good collision statistics, needed less code & used less memory.

*/'''

class Entry(object):
    """
    A hash table entry.

    Attributes:
       * key - The key for this entry.
       * hash - The has of the key.
       * value - The value associated with the key.
    """
    __slots__ = ("key", "value", "hash")
    
    def __init__(self):
        self.key = None
        self.value = None
        self.hash = 0
    
    def __repr__(self):
        return str(self.key) + " : " + str(self.value)


class Dict(object):
    """
    A mapping interface implemented as a hash table.

    Attributes:
        * used - The number of entires used in the table.
        * filled - used + number of entries with a dummy key.
        * table - List of entries; contains the actual dict data.
        * mask - Length of table - 1. Used to fetch values.
    """
    
    __slots__ = ("filled","used","mask","table")
    
    def __init__(self, args, **kwargs):
        self.init()
        self._update(arg, kwargs)
    
    def init(self):
        ''' Initialize an empty dict '''
        self.filled = 0
        self.used = 0
        self.table = []
        self.mask = MINSIZE - 1
        for i in range(MINSIZE):
            self.table.append(Entry())
        
    
    def pop(self, *args):
        '''
        Remove and return the value for a key.
        '''
        default = len(args) == 2
        try:
            my_val = self[args[0]]  ### Q: why does this work?  A: __getitem__(self, key) is defined to use self._lookup(key).  Syntactic sugar at its sweetest.
        except KeyError as k:
            if default:
                return args[1]
            else:
                raise KeyError from k
        del self[args[0]]
        return my_val
    
    def popitem(self):
        '''
        Remove and return an arbitrary (key, value) pair from the dictionary.
        popitem() is useful to destructively iterate over a dictionary, as often used in set algorithms. 
        If the dictionary is empty, calling popitem() raises a KeyError.
        '''
        if self.used == 0:
            raise KeyError("cannot pop from an empty dict")
        else:
            # find the first non-empty slot by linear search, remove it from the dict
            i = 0
            first_entry = self.table[i]
            val = first_entry.value
            if val is None:
                i = first_entry.hash
                if i > self.mask or i < i:
                    i = 1
                    entry = self.table[i]
                while entry.value is not None:
                    i += 1
                    if i > self.mask:
                        i = 1
                    entry = self.table[i]                    
            arb = entry.key, entry.value
            self._del(entry)
            return arb
            
        
    def setdefault(self, key, default=0):
        """
        If key is in the dictionary, return it. Otherwise, set it to the default
        value.
        """
        entry = self._lookup(key)
        if entry.value is None:
            entry.value = default
            return default
        else:
            return entry.value
        
    def _lookup(self, key):
        ''' Find the key for entry '''
        # hash the key, examine entry
        key_hash = hash(key)
        index = key_hash & self.mask
        entry = self.table[index]
        if entry.key is None or entry.key is key:
            return entry
        # introduce the notion of 'free' nodes which used to hold entries, but have since been deleted.
        free = None
        if entry.key == dummy:
            free = entry
        # or entry might already be a valid element of the dict
        elif entry.hash == key_hash and key == entry.key:
            return entry
        
        # none of the above, and entry cannot be used, perturb the hash to find the next best place
        perturb = key_hash
        while True:
            # generate new index, retrieve entry at index
            index = (index << 2) + index + perturb + 1;
            entry = self.table[index & self.mask]            
            
            # test for suitable entry
            if free is not None:      # encountered a dummy key in last entry, use it.
                return free
            elif entry.key is None:   # empty spot, use it.
                return entry
            elif entry.key is key or (entry.hash == key_hash and key == entry.key):
                return entry        # already in the dict
            elif entry.key is dummy and free is None:
                free = entry
        
        

    def _resize(self, minused):
        """
        Resize the dictionary to at least minused.
        """
        # find the smallest value for new table size
        newsize = MINSIZE
        while newsize <= minused:
            newsize <<= 1
        
        # create the new table, populate with empty entries
        new_table = []
        while len(new_table) <= newsize:
            new_table.append(Entry())

        # replace the old table with the new table
        old_table = self.table
        self.table = new_table
        self.used = 0
        self.filled = 0
        
        # copy over entries from the old table into the new table
        for entry in old_table:
            if entry.value is not None:
                self._insert_into_clean(entry)
            elif entry.key == dummy:
                entry.key = None
        self.mask = newsize - 1
    
    def _insert_into_clean(self, entry):
        """
        Insert an item in a clean dict. This is a helper for resizing.
        """
        i = entry.hash & self.mask
        temp_entry = self.table[i]
        perbturb = entry.hash
        while temp_entry.key is not None:       # probe for an empty entry
            i = (i << 2) + i + perturb + 1
            temp_entry = self.table[i & self.mask]
            perturb = perturb >> PERTURB_SHIFT
        temp_entry.key = entry.key
        temp_entry.value = entry.value
        temp_entry.hash = entry.hash
        self.used += 1
        self.filled += 1
    

    def _insert(self, key, value):
        """
        Add a new value to the dictionary or replace an old one.
        """
        entry = self._lookup(key)
        if entry.value == None:
            self.used += 1
            if entry.key is not dummy:
                self.filled += 1            
        entry.key = key
        entry.value = value
        entry.hash = hash(key)    
                        

    def _del(self, entry):
        """
        Mark an entry as free with the dummy key.
        """
        entry.key = dummy
        entry.value = None
        self.used -= 1

    def __getitem__(self, key):
        ''' Get the value associated with the given key, or raise a KeyError'''
        entry = self._lookup(key)
        if entry.value is None:
            raise KeyError("not present in keys: {0!r}".format(key))
        else:
            return entry.value        
        
        
    def __setitem__(self, key, what):
        ''' Create or update a new entry '''
        # None is used as a marker for empty entries, so it can't be in a
        # dictionary.
        assert what is not None and key is not None, \
               "key and value must not be None"
        old_used = self.used
        self._insert(key, what)
        # Maybe resize the dict.
        if not (self.used > old_used and
                self.filled * 3 >= (self.mask + 1)*2):   # avoid division when possible.
            return
        # Large dictionaries (< 5000) are only doubled in size.
        factor = 2 if self.used > 5000 else 4
        self._resize(factor*self.used)

    def __delitem__(self, key):
        entry = self._lookup(key)
        if entry.value is None:
            raise KeyError("no such key: {0!r}".format(key))
        self._del(entry)

    def __contains__(self, key):
        """
        Check if a key is in the dictionary.
        """
        entry = self._lookup(key)
        return entry is not None
            

    def __eq__(self, other):
        pass

    def __ne__(self, other):
        return not self == other

    def keys(self):
        """
        Return a list of keys in the dictionary.
        """
        return [entry.key for entry in self.table if entry.value is not None]

    def values(self):
        """
        Return a list of values in the dictionary.
        """
        return [entry.value for entry in self.table if entry.value is not None]

    def items(self):
        """
        Return a list of key-value pairs.
        """
        return [(entry.key, entry.value) for entry in self.table if entry.value is not None]

    def __iter__(self):
        """ Return an iterator over keys """
        pass
    

    def itervalues(self):
        """
        Return an iterator over the values in the dictionary.
        """
        pass

    def iterkeys(self):
        """
        Return an iterator over the keys in the dictionary.
        """
        pass

    def iteritems(self):
        """
        Return an iterator over key-value pairs.
        """
        pass

    def _merge(self, mapping):
        """
        Update the dictionary from a mapping.
        """
        for key in mapping.keys():
            self[key] = mapping[key]
            

    def _from_sequence(self, seq):
        ''' Update values in the dictionary from a sequence of 2-ary key, value pairs.  '''
        for double in seq:
            if len(double) != 2:
                raise ValueError("{0!r} doesn't have a length of 2".format(
                    double))
            self[double[0]] = double[1]
        pass

    def _update(self, arg, kwargs):
        ''' Internal method to update a dict from a mapping or sequence object '''
        if arg:
            if isinstance(arg, collections.Mapping):
                self._merge(arg)
            else:
                self._from_sequence(arg)
        if kwargs:
            self._merge(kwargs)
        pass

    def update(self, arg=None, **kwargs):
        """
        Update the dictionary from a mapping or sequence containing key-value
        pairs. Any existing values are overwritten.
        """
        self._update(arg, kwargs)

    def get(self, key, default=0):
        """
        Return the value for key if it exists otherwise the default.
        """
        try:
            return self[key]
        except KeyError:
            return default

    def __len__(self):
        return self.used

    def __repr__(self):
        r = ["{0!r} : {1!r}".format(k, v) for k, v in self.iteritems()]
        return "Dict({" + ", ".join(r) + "})"