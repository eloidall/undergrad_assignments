

public class Customer  {

	private String name;
	private int  targetTipPct;

	public Customer(String name, int targetTipPct) {
		this.name = name;
		this.targetTipPct = targetTipPct;
	}

	public String getName() {
		return name;
	}

	public int getTargetTipPct() {
		return targetTipPct;
	}

	public String getDescriptiveMessage(FoodPlace foodPlace) {
		return this.name + " dined in " + foodPlace.getName();
	}



	public void dineAndPayCheck(FoodPlace foodPlace, double menuPrice ) {
		// To calculate the ActualTipPct
		double targetTipPctCustomer = targetTipPct;
		double ActualTipPct = (foodPlace.getTipPercentage() + targetTipPctCustomer) / 2;
		// To construct the Check accordingly
		Check check = new Check(menuPrice);
		check.setTipByPct(ActualTipPct);
		// To distribute the earnings of the check
		foodPlace.distributeIncomeAndSalesTax(check);
	}
}