
public class Staff extends IncomeTaxPayer {

	private int salaryPerHour;
	final private int incomeTaxPercentage = 25;

	public Staff(String name, boolean isCook) {
		super(name);
		if (isCook){
			this.salaryPerHour = 20;
		}else{
			this.salaryPerHour = 10;
		}
	}

	public int getSalaryPerHour() {
		return salaryPerHour;
	}

	public int getIncomeTaxPercentage() {
		return incomeTaxPercentage;
	}

	public double workHours(int numHours) {
		double incomeEarned = numHours * salaryPerHour;
		this.setIncome(this.getIncome() + incomeEarned);
		return incomeEarned;
	}

	@Override
	public double calculateIncomeTax() {
		return ((this.getIncome() * incomeTaxPercentage) / 100);
	}
}