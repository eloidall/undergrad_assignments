import java.util.LinkedList;

public class Memory {

    // Memory class fields
    public char[] memoryArray;
    public static int idCount;
    public LinkedList<StringInterval> intervalList;

    // Memory class constructor
    public Memory(int n) {
        memoryArray = new char[n];
        idCount = 0;
        intervalList = new LinkedList<StringInterval>();
    }

    // Class methods
    public String get(int id) {
        /**
         * Returns the string obj corresponding to the given id found, otherwise returns null.
         */
        for (StringInterval str : intervalList){
            if (id == str.id){
                char str_obj = memoryArray[str.start];
                String final_str = "";
                for (int i = str.start; i < (str.start + str.length); i++){
                    final_str += str_obj;
                    if ((i+1) < memoryArray.length) {
                        str_obj = memoryArray[i+1];
                    }
                }
                return final_str;
            }
        }
        return null;
    }

    public int get(String s) {
        /**
         * Returns the string s (exact element) id if found, otherwise -1.
         */
        for (StringInterval str : intervalList) {
            // To verify it is related to a StringInterval obj
            if (str.length == s.length()) {
                // To verify if exact same string
                String str_obj = this.get(str.id);
                if (str_obj.equals(s)) {
                    return str.id;
                }
            }
        }
        return -1;
    }

    public int remove(String s) {
        /**
         * Removes the string corresponding to the given string.
         * Returns the id of the string found or -1 otherwise.
         */
        // To verify if associated with a found obj
        int s_id = this.get(s);
        if (s_id != -1){
            this.remove(s_id);
            return s_id;
        }
        return s_id;
    }

    public String remove(int id) {
        /**
         * Removes the string corresponding to the given id.
         * Returns the JAVA string obj found or otherwise null.
         */
        // To check if associated with proper obj
        for (StringInterval str : intervalList){
            if (id == str.id) {
                // To remove the obj
                String str_id = this.get(id);
                intervalList.remove(str);
                return str_id;
            }
        }
        return null;
    }

    public void defragment() {
        /**
         * Gets rid of gaps in memory by ensuring that the first one
         * starts at memory 0 and that there's no gaps further along.
         * Returns: void. Chars must not be erased after.
         */
        int counter = 0;
        for (StringInterval str : intervalList) {
            // If no empty spots
            if (str.start == counter){
                counter += str.length;
                continue;
            }
            // To restore chars with proper start value if needed
            String str_obj = this.get(str.id);
            int shift = str.start - counter;
            for (int i = 0; i < (str.length); i++){
                memoryArray[(i + str.start) - shift] = memoryArray[i + str.start];
            }
            // To update str.start and keep on going
            str.start = counter;
            counter = str.start + str.length;
        }
    }

    public int put(String s) {
        /**
         * Adds new string to memory at first available location.
         * If no room available, should call defragment() and then stores string at the end.
         * Returns string id if successful or -1 otherwise.
         */
        // To initialize future instance fields
        int id = idCount;
        int start = -1;
        // To keep track of the appropriate linkedList position
        int list_position = -1;

        // If intervalList EMPTY
        if (intervalList.isEmpty()){
            // If s fits in memoryArray
            if (s.length() <= memoryArray.length){
                // To update variables
                start = 0;
                list_position = 0;
                // If s doesn't fit
            }else{
                return start;
            }

            // If intervalList NOT EMPTY
        }else{
            // To verify if s fits between the current and next str
            int counter = 0;
            for (StringInterval str : intervalList) {
                // If the next spot is not available in memoryArray
                if (str.start == counter) {
                    counter += str.length;
                }
                // If the first element is not starting at 0
                if (str.equals(intervalList.getFirst())){
                    if((str.start - counter) > s.length()){
                        start = counter;
                        list_position = 0;
                        continue;
                    }
                }
                // If its last element of intervalList
                if (str.equals(intervalList.getLast())){
                    int str_stop = str.start + str.length;
                    if (s.length() <= (memoryArray.length - str_stop)) {
                        // To update variables
                        start = str_stop;
                        list_position = intervalList.size();
                        continue;
                    }
                }
                // If there's room available and it fits
                if ((str.start - counter) > s.length()) {
                    // To update variables
                    start = counter;
                    list_position = intervalList.indexOf(str);
                }
            }
        }

        // Defragment if no memory gap available
        if(start == -1) {
            this.defragment();
            // Check if room available at end of memoryArray
            int tailStop = intervalList.getLast().start + intervalList.getLast().length;
            // If room at the end
            if (s.length() <= (memoryArray.length - tailStop)) {   // TODO: might be shorter
                // To update variables
                start = tailStop;
                list_position = intervalList.size();
                // If no room at end
            } else {
                return start;
            }
        }
        // Create the StringInterval obj and add it to intervalList
        StringInterval w = new StringInterval(id, start, s.length());
        // If added at the end
        if (list_position == intervalList.size()){
            intervalList.addLast(w);
            // Otherwise
        }else{
            intervalList.add(list_position, w);
        }

        // Properly store char of s in the memoryArray
        char[] char_array = s.toCharArray();
        for (int i = 0; i < char_array.length; i++){
            memoryArray[w.start + i] = char_array[i];
        }
        // To update idCount and return the id of last element added
        idCount += 1;
        return idCount - 1;
    }

    public class StringInterval {
        // Inner class fields
        public int id;
        public int start;
        public int length;

        // Inner class constructor
        public StringInterval(int id, int start, int length) {
            this.id = id;
            this.start = start;
            this.length = length;
        }
    }

    // TEST
    public static void main(String[] args) {}
}