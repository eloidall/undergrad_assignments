import java.util.Iterator;
import java.util.ArrayList;


class TSTIterator<T extends Comparable<T>> implements Iterator<T> {
    // To initialize the ordered list used by the iterator
    ArrayList<T> IteratorList = new ArrayList<>();
    Iterator<T> itr;

    // Constructor
    public TSTIterator(TSTNode<T> root){
        this.getIteratorList(root);
        this.itr = IteratorList.iterator();
    }
    /**
     * Returns {@code true} if the iteration has more elements. (In other words, returns {@code true} if {@link #next}
     * would return an element rather than throwing an exception.)
     *
     * @return {@code true} if the iteration has more elements
     */
    @Override
    public boolean hasNext() { return itr.hasNext(); }

    /**
     * Returns the next element in the iteration.
     *
     * @return the next element in the iteration
     *
     * //@throws NoSuchElementException
     *         if the iteration has no more elements
     */
    @Override
    public T next(){
        return itr.next();
    }
    // Helper method
    public void getIteratorList (TSTNode<T> root) {
        if (root != null) {
            getIteratorList(root.left);
            IteratorList.add(root.element);
            getIteratorList(root.mid);
            getIteratorList(root.right);
        }
    }
}