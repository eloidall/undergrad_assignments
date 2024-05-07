import java.util.LinkedList;

class TSTNode<T extends Comparable<T>> {
    T element;                    // The data in the node
    TSTNode<T> left;        // left child
    TSTNode<T> mid;            // middle child
    TSTNode<T> right;        // right child

    TSTNode(T element) {
        this.element = element;
        this.left = null;
        this.right = null;
        this.mid = null;
    }
    TSTNode<T> findMax() { return findMax_helper(this);}

    TSTNode<T> findMin() { return findMin_helper(this);}

    int height(){ return height_helper(this);}

    // Helper methods
    TSTNode<T> findMax_helper(TSTNode<T> root){
        if (root == null) {
            return null;
        } else if (root.right == null) {
            return root;
        } else {
            return findMax_helper(root.right);
        }
    }
    TSTNode<T> findMin_helper(TSTNode<T> root){
        if (root == null) {
            return null;
        } else if (root.left == null) {
            return root;
        } else {
            return findMin_helper(root.left);
        }
    }
    public int height_helper(TSTNode<T> root){
        if ( (root == null) || (getChildrenList(root).size() == 0) ) {
            return 0;
        } else {
            int treeHeight = 0;
            for (TSTNode<T> child : getChildrenList(root))
                treeHeight = Math.max(treeHeight, height_helper(child));
            return 1 + treeHeight;
        }
    }
    LinkedList<TSTNode<T>> getChildrenList(TSTNode<T> root){
        LinkedList<TSTNode<T>> childrenList = new LinkedList<>();
        if (root.left != null){
            childrenList.add(root.left);
        }
        if (root.mid != null){
            childrenList.add(root.mid);
        }
        if (root.right != null){
            childrenList.add(root.right);
        }
        return childrenList;
    }
}



