
public abstract class IncomeTaxPayer {

	private static int currentMaxTaxID;
	private int  taxID;
	private String  name;
	private double  income;

	public IncomeTaxPayer(String name){
		this.currentMaxTaxID += 1;
		this.taxID = currentMaxTaxID;
		this.name = name;
	}

	public static int getCurrentMaxTaxID() {
		return currentMaxTaxID;
	}

	public int getTaxID() {
		return taxID;
	}

	public String getName() {
		return name;
	}

	public double getIncome() {
		return this.income;
	}

	public void setIncome( double income) {
		this.income = income;
	}

	public String toString() {
		return "  " + taxID + " " + name + " income " + income ;
	}

	public boolean equals(Object obj) {
		//Verify if the obj argument is an IncomeTaxPayer and id is matching
		if (obj == this){
			return true;
		}
		if (obj == null || obj.getClass() != this.getClass()){
			return false;
		}
		return ((IncomeTaxPayer) obj).taxID == this.taxID;
	}

	public abstract double calculateIncomeTax();
}