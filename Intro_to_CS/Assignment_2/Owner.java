
public class Owner extends IncomeTaxPayer {

	final private int incomeTaxPct = 10;
	private double salaryExpenses;

	private FoodPlace foodPlace;

	public Owner(String name) {
		super(name);
	}

	public int getIncomeTaxPct() {
		return incomeTaxPct;
	}

	public double getSalaryExpenses() {
		return salaryExpenses;
	}

	public void setSalaryExpenses(double salaryExpenses) {
		this.salaryExpenses = salaryExpenses;
	}

	public FoodPlace getFoodPlace(){return foodPlace; }

	public void setFoodPlace(FoodPlace foodPlace) {
		this.foodPlace = foodPlace;
	}

	@Override
	public double calculateIncomeTax() {
		double profit = this.getIncome() - this.foodPlace.getFixedCosts() - this.salaryExpenses;
		if (profit > 0){
			return (profit * incomeTaxPct / 100);
		}else{
			return 0;
		}
	}
}