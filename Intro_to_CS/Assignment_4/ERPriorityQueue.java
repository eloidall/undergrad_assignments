import java.util.ArrayList;
import java.util.HashMap;

public class ERPriorityQueue {

	public ArrayList<Patient> patients;
	public HashMap<String, Integer> nameToIndex;

	public ERPriorityQueue() {
		//  use a dummy node so that indexing starts at 1, not 0
		patients = new ArrayList<Patient>();
		patients.add(new Patient("dummy", 0.0));
		nameToIndex = new HashMap<String, Integer>();
	}

	private int parent(int i) {
		return i / 2;
	}

	private int leftChild(int i) {
		return 2 * i;
	}

	private int rightChild(int i) {
		return 2 * i + 1;
	}

	// HELPER METHODS
	public static <T> void swapList(ArrayList<T> list, int i, int j) {
		T temp = list.get(i);
		list.set(i, list.get(j));
		list.set(j, temp);
	}

	public static <K, V> void swapHashMapValues(HashMap<K, V> hashMap, K key1, K key2) {
		V temp = hashMap.get(key1);
		hashMap.put(key1, hashMap.get(key2));
		hashMap.put(key2, temp);
	}

	public boolean isEmpty() {
		return this.patients.size() == 1;
	}

	public boolean isLeaf(int i) {            //TODO: "<" or "<=" ??
		return (this.leftChild(i) <= patients.size());
	}

	public static ArrayList<Patient> makeDeepCopy(ArrayList<Patient> list) {
		ArrayList<Patient> copy = new ArrayList<Patient>();
		for (Patient patient : list) {
			copy.add(new Patient(patient.getName(), patient.getPriority()));
		}
		return copy;
	}

	// METHODS
	public void upHeap(int i) {
		while ((i > 1) && (this.patients.get(i).getPriority() < this.patients.get(i / 2).getPriority())) {
			swapList(this.patients, i, i / 2);
			swapHashMapValues(nameToIndex, patients.get(i).getName(), patients.get(i / 2).getName());
			i = i / 2;
		}
	}

	public void downHeap(int i) {
		while (2 * i <= patients.size() - 1) {
			int child = 2 * i;
			// If there's a right child
			if (child < patients.size() - 1) {
				// To choose smaller child
				if (patients.get(child + 1).getPriority() < patients.get(child).getPriority()) {
					child++;
				}
			} // Swap with child if necessary
			if (patients.get(child).getPriority() <= patients.get(i).getPriority()) {
				swapHashMapValues(nameToIndex, patients.get(i).getName(), patients.get(child).getName());
				swapList(patients, i, child);
				i = child;
			} else return;
		}
	}

	public boolean contains(String name) {
		if (patients.isEmpty()) {
			return false;
		}
		return nameToIndex.get(name) != null;
	}

	public double getPriority(String name) {
		if (this.contains(name)) {
			return patients.get(nameToIndex.get(name)).getPriority();
		} else return -1;
	}

	public double getMinPriority() {
		if (this.isEmpty()) {
			return -1;
		} else return patients.get(1).getPriority();
	}

	public String removeMin() {
		if (this.isEmpty()) {
			return null;
		} else {
			// To store initial stage
			Patient toRemove = patients.get(1);
			int lastIndex = patients.size() - 1;
			Patient last = patients.get(lastIndex);

			// To swap first and last element
			swapList(patients, 1, lastIndex);
			swapHashMapValues(nameToIndex, toRemove.getName(), last.getName());
			// To clear the last element and downHeap()
			patients.remove(lastIndex);
			nameToIndex.remove(toRemove.getName());
			this.downHeap(1);
			// To return the removed name
			return toRemove.getName();
		}
	}

	public String peekMin() {
		if (this.isEmpty()) {
			return null;
		} else return patients.get(1).getName();
	}

	public boolean add(String name, double priority) {
		if (this.contains(name)) {
			return false;
		} else {
			Patient patient = new Patient(name, priority);
			patients.add(patient);
			nameToIndex.put(patient.getName(), patients.size() - 1);
			this.upHeap(patients.size() - 1);
			return this.contains(name);
		}
	}

	public boolean add(String name) {
		return this.add(name, Double.POSITIVE_INFINITY);
	}

	public boolean remove(String name) {
		if (!this.contains(name)) {
			return false;
		} else {
			// To store initial stage
			int toRemoveIndex = nameToIndex.get(name);
			Patient toRemove = patients.get(toRemoveIndex);
			int lastIndex = patients.size() - 1;
			Patient last = patients.get(lastIndex);

			// To swap toRemove and last element
			swapList(patients, toRemoveIndex, lastIndex);
			swapHashMapValues(nameToIndex, toRemove.getName(), last.getName());
			// To clear the last element and downHeap()
			patients.remove(lastIndex);
			nameToIndex.remove(toRemove.getName());
			this.downHeap(toRemoveIndex);
			return !this.contains(name);
		}
	}

	public boolean changePriority(String name, double priority) {
		if (!this.contains(name)) {
			return false;
		} else {
			if (priority != this.getPriority(name)) {
				// To modify priority if different and replace element accordingly
				patients.get(nameToIndex.get(name)).setPriority(priority);
				this.upHeap(nameToIndex.get(name));
				this.downHeap(nameToIndex.get(name));
			}
			return true;
		}
	}

	public ArrayList<Patient> removeUrgentPatients(double threshold) {
		ArrayList<Patient> removedPatient = new ArrayList<Patient>();
		for (Patient patient : this.patients) {
			if ((patient.getPriority() != 0.0) && (patient.getPriority() <= threshold)) {
				removedPatient.add(patient);
			}
		}
		for (Patient patient : removedPatient) {
			this.remove(patient.getName());
		}
		return removedPatient;
	}

	public ArrayList<Patient> removeNonUrgentPatients(double threshold) {
		ArrayList<Patient> removedPatient = new ArrayList<Patient>();
		for (Patient patient : this.patients) {
			if (patient.getPriority() >= threshold) {
				removedPatient.add(patient);
			}
		}
		for (Patient patient : removedPatient) {
			this.remove(patient.getName());
		}
		return removedPatient;
	}

	// INNER CLASS
	static class Patient {
		private String name;
		private double priority;

		Patient(String name, double priority) {
			this.name = name;
			this.priority = priority;
		}

		Patient(Patient otherPatient) {
			this.name = otherPatient.name;
			this.priority = otherPatient.priority;
		}

		double getPriority() {
			return this.priority;
		}

		void setPriority(double priority) {
			this.priority = priority;
		}

		String getName() {
			return this.name;
		}

		@Override
		public String toString() {
			return this.name + " - " + this.priority;
		}

		public boolean equals(Object obj) {
			if (!(obj instanceof ERPriorityQueue.Patient)) return false;
			Patient otherPatient = (Patient) obj;
			return this.name.equals(otherPatient.name) && this.priority == otherPatient.priority;
		}
	}
}