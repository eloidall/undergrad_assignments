import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

public class TST<T extends Comparable<T>> implements Iterable<T>{
    TSTNode<T> root;
    ArrayList<T> IteratorList = new ArrayList<T>();
    ArrayList<T> balancedOrder = new ArrayList<T>();

    // Constructor
    public TST() {
        this.root = null;
    }

    // Methods
    public void insert(T element){ root = insert_helper(root, element); }

    public void remove(T element){ root = remove_helper(root, element); }

    public boolean contains(T element){ return contains_helper(root, element); }

    public void rebalance(){
        // Create an arraylist of sorted element of the tree
        ArrayList<T> sortedList = this.getIteratorList(this.root);
        // Build balanced tree with helper
        this.root = rebalance_helper(sortedList);
    }

    // Helper methods
    public TSTNode<T> insert_helper(TSTNode<T> root, T element){
        if (root == null){
            root = new TSTNode<>(element);
            return root; }
        // To adequately insert the element in the tree
        if (element.compareTo(root.element) < 0){
            root.left = insert_helper(root.left, element);
        }
        else if (element.compareTo(root.element) > 0){
            root.right = insert_helper(root.right, element);
        }
        // If the element is equal to the root
        else{
            root.mid = insert_helper(root.mid, element);
        }
        return root;
    }
    public TSTNode<T> remove_helper(TSTNode<T> root, T element){
        if (root == null){
            return null;
        } // On the left side
        else if (element.compareTo(root.element) < 0){
            root.left = remove_helper(root.left, element);
        } // On the right side
        else if (element.compareTo(root.element) > 0){
            root.right = remove_helper(root.right, element);
        } // Found
        else{
            if (root.mid != null){
                root.element = root.mid.element;
                root.mid = remove_helper(root.mid, root.element);
            }
            else if (root.left == null){
                root = root.right;
            }
            else if (root.right == null){
                root = root.left;
            } // Both left and right child
            else{
                root.element = root.left.findMax().element;
                root.left = remove_helper(root.left, root.element);
            }
        }
        return root;
    }
    public boolean contains_helper(TSTNode<T> root, T element) {
        if (root == null) {
            return false;
        } else if (element.equals(root.element)) {
            return true;
        } else if (element.compareTo(root.element) < 0) {
            return contains_helper(root.left, element);
        } else{
            return contains_helper(root.right, element);
        }
    }
    public TSTNode<T> rebalance_helper(List<T> sortedList){
        // Create an arrayList of the order the balanced tree should be build
        if (sortedList.size() >= 1) {
            int separator = sortedList.size() / 2;
            this.balancedOrder.add(sortedList.get(separator));
            // Recursion for both left and right subList
            List<T> left_subList = sortedList.subList(0, separator);
            rebalance_helper(left_subList);
            List<T> right_subList = sortedList.subList(separator + 1, sortedList.size());
            rebalance_helper(right_subList);
        }
        // Create balanced tree
        TST<T> balancedTree = new TST<T>();
        for (T element : this.balancedOrder) {
            balancedTree.insert(element);
        }
        return balancedTree.root;
    }
    public ArrayList<T> getIteratorList(TSTNode<T> root){
        if (root != null) {
            getIteratorList(root.left);
            IteratorList.add(root.element);
            getIteratorList(root.mid);
            getIteratorList(root.right);
        }
        return IteratorList;
    }
    /**
     * Caculate the height of the tree.
     * You need to implement the height() method in the TSTNode class.
     *
     * @return -1 if the tree is empty otherwise the height of the root node
     */
    public int height(){
        if (this.root == null)
            return -1;
        return this.root.height();
    }
    /**
     * Returns an iterator over elements of type {@code T}.
     *
     * @return an Iterator.
     */
    @Override
    public Iterator iterator(){
        return new TSTIterator<T>(this.root); }

    // --------------------PROVIDED METHODS--------------------
    // The code below is provided to you as a simple way to visualize the tree
    // This string representation of the tree mimics the 'tree' command in unix
    // with the first child being the left child, the second being the middle child, and the last being the right child.
    // The left child is connect by ~~, the middle child by -- and the right child by __.
    // e.g. consider the following tree
    //               5
    //            /  |  \
    //         2     5    9
    //                   /
    //                  8
    // the tree will be printed as
    // 5
    // |~~ 2
    // |   |~~ null
    // |   |-- null
    // |   |__ null
    // |-- 5
    // |   |~~ null
    // |   |-- null
    // |   |__ null
    // |__ 9
    //     |~~ 8
    //     |   |~~ null
    //     |   |-- null
    //     |   |__ null
    //     |-- null
    //     |__ null
    @Override
    public String toString() {
        if (this.root == null)
            return "empty tree";
        // creates a buffer of 100 characters for the string representation
        StringBuilder buffer = new StringBuilder(100);
        // build the string
        stringfy(buffer, this.root,"", "");
        return buffer.toString();
    }
    /**
     * Build a string representation of the tertiary tree.
     * @param buffer String buffer
     * @param node Root node
     * @param nodePrefix The string prefix to add before the node's data (connection line from the parent)
     * @param childrenPrefix The string prefix for the children nodes (connection line to the children)
     */
    private void stringfy(StringBuilder buffer, TSTNode<T> node, String nodePrefix, String childrenPrefix) {
        buffer.append(nodePrefix);
        buffer.append(node.element);
        buffer.append('\n');
        if (node.left != null)
            stringfy(buffer, node.left,childrenPrefix + "|~~ ", childrenPrefix + "|   ");
        else
            buffer.append(childrenPrefix + "|~~ null\n");
        if (node.mid != null)
            stringfy(buffer, node.mid,childrenPrefix + "|-- ", childrenPrefix + "|   ");
        else
            buffer.append(childrenPrefix + "|-- null\n");
        if (node.right != null)
            stringfy(buffer, node.right,childrenPrefix + "|__ ", childrenPrefix + "    ");
        else
            buffer.append(childrenPrefix + "|__ null\n");
    }
    /**
     * Print out the tree as a list using an enhanced for loop.
     * Since the Iterator performs an inorder traversal, the printed list will also be inorder.
     */
    public void inorderPrintAsList(){
        String buffer = "[";
        for (T element: this) {
            buffer += element + ", ";
        }
        int len = buffer.length();
        if (len > 1)
            buffer = buffer.substring(0,len-2);
        buffer += "]";
        System.out.println(buffer);
    }


    public static void main(String[] args) {
//
//        // With different comparable obj
//        TST<String> tree = new TST<String>();
//        tree.insert("a");
//        tree.insert("b");
//        tree.insert("j");
//        tree.insert("p");
//        tree.insert("b");
//        tree.insert("q");
//        tree.insert("a");
//        System.out.println(tree.toString());
//
//        tree.rebalance();
//
//        if (tree.root.element.equals("b") &&
//                tree.root.mid.element.equals("b") &&
//                tree.root.right.element.equals("p") &&
//                tree.root.right.left.element.equals("j") &&
//                tree.root.right.right.element.equals("q") &&
//                tree.root.left.element.equals("a") &&
//                tree.root.left.mid.element.equals("a")) {
//            System.out.println("NICE :D");
//        } else {
//            System.out.println("Double check to make sure your TST works with all comparable objects :p");
//        }

        //Here is a removal test for if both left and right !=null and the largest element
        //in the left tree has 3 duplicates.
//        TST<Integer> tree=new TST<Integer>();
//        tree.insert(45);
//        tree.insert(15);
//        tree.insert(23);
//        tree.insert(7);
//        tree.insert(9);
//        tree.insert(9);
//        tree.insert(9);
//        tree.insert(5);
//        tree.remove(15);
//        TSTNode<Integer> root = tree.root;
//
//        if(root.element==45&root.left.element==9&root.left.mid.element==9&&
//                root.left.mid.mid.element==9&root.left.right.element==23&&root.left.left.element==7){
//            System.out.println("pass");
//        }else{
//            System.out.println("fail");
//        }

        // Remove() with middle children
//        TST<Integer> myTree = new TST<Integer>();
//
//        myTree.insert(6);
//        myTree.insert(8);
//        myTree.insert(4);
//        myTree.insert(4);
//        myTree.insert(5);
//        myTree.insert(3);
//        myTree.insert(9);
//        myTree.insert(3);
//        myTree.insert(-1);
//        myTree.insert(2);
//        System.out.println(myTree.toString());
//
//
//        myTree.remove(4);
//
//        System.out.println(myTree.toString());

        // Remove() with duplicates, making sure only one instance is removed
//        TST<Integer> tree = new TST<>();
//        tree.insert(5);
//        tree.insert(5);
//        tree.insert(5);
//        tree.remove(5);
//        tree.remove(5);
//        tree.remove(5);
//
//        // By now, the tree should be empty
//        if (tree.height() != -1) {
//            System.out.println("Remove doesn't work properly");
//        }
//        else System.out.println("Good job");

        // Remove() when both left and right children
//        TST<Integer> tree = new TST<Integer>();
//
//        tree.insert(3);
//        tree.insert(0);
//        tree.insert(0);
//        tree.insert(0);
//        tree.insert(7);
//        tree.insert(8);
//        tree.insert(-1);
//        tree.insert(-1);
//        tree.remove(3);
//
//        if (tree.root.element == 0 &&
//                tree.root.mid.element == 0 &&
//                tree.root.mid.mid.element == 0 &&
//                tree.root.left.element == -1 &&
//                tree.root.left.mid.element == -1 &&
//                tree.root.right.element == 7 &&
//                tree.root.right.right.element == 8) {
//            System.out.println("All good!");
//        } else {
//            System.out.println("Check your remove method, specifically the case where the root has both right and left references and refer to #814 on ed.");
//        }



    }


}