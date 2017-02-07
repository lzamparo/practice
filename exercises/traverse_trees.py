from binary_tree_node import BinaryTreeNode

def build_balanced_tree():
    root = BinaryTreeNode(5)
    root.set_left(BinaryTreeNode(3))
    root.set_right(BinaryTreeNode(9))
    root.get_left().set_left(BinaryTreeNode(1))
    root.get_left().set_right(BinaryTreeNode(4))
    root.get_right().set_left(BinaryTreeNode(7))
    root.get_right().set_right(BinaryTreeNode(11))
    return root

def pre_order_traversal(node):
    if node is not None:
        node.visit()
        pre_order_traversal(node.get_left())
        pre_order_traversal(node.get_right())
    else:
        return None

def in_order_traversal(node):
    if node is not None:
        in_order_traversal(node.get_left())
        node.visit()
        in_order_traversal(node.get_right())
    else:
        return None

def post_order_traversal(node):
    if node is not None:
        post_order_traversal(node.get_left())
        post_order_traversal(node.get_right())
        node.visit()
    else:
        return None

    
def drive_traversals():
    root = build_balanced_tree()
    print("pre-order traversal: ")
    pre_order_traversal(root)
    print("---------------------")
    root = build_balanced_tree()
    print("in-order traversal: ")
    in_order_traversal(root)
    print("---------------------")
    root = build_balanced_tree()
    print("post-order traversal")
    post_order_traversal(root)
    print("---------------------")