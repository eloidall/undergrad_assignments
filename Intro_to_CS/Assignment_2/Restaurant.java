
import java.util.ArrayList;
import java.util.List;

public class Restaurant extends FoodPlace {

	private Staff cook;
	private Server server;

	public Restaurant(String name, double fixedCosts, Owner owner, Staff cook, Server server) {
		super(name,fixedCosts,owner);
		this.cook = cook;
		this.server = server;
	}

	public Staff getCook() {
		return cook;
	}

	public Server getServer() {
		return server;
	}

	@Override
	public String toString() {
		return "Name of restaurant: " + this.getName() +
				"\n" + "Owner: " + this.getOwner() +
				"\n" + "Cook: " + cook +
				"\n" + "Server: " + server;
	}

	@Override
	public void workShift(int hours) {
		// To update the Staff income
		cook.workHours(hours);
		server.workHours(hours);
		// To update the owner's Salary Expenses
		double salaryExpenses = hours * (cook.getSalaryPerHour() + server.getSalaryPerHour());
		this.getOwner().setSalaryExpenses(salaryExpenses);
	}

	@Override
	public List<IncomeTaxPayer> getIncomeTaxPayers() {
		// To return a list of all the IncomeTaxPayers of the Restaurant
		ArrayList<IncomeTaxPayer> IncomeTaxPayersList = new ArrayList<IncomeTaxPayer>(3);
		IncomeTaxPayersList.add(this.getOwner());
		IncomeTaxPayersList.add(this.cook);
		IncomeTaxPayersList.add(this.server);
		return IncomeTaxPayersList;
	}

	@Override
	public void distributeIncomeAndSalesTax(Check check) {
		// To update the owner's income with the menu price
		this.getOwner().setIncome(this.getOwner().getIncome() + check.getMenuPrice());
		// To update the Staff's income with their tip
		this.cook.setIncome(this.cook.getIncome() + (check.getTip() * 0.20));
		this.server.setIncome(this.server.getIncome() + (check.getTip() * 0.80));
		// To update the Restaurant totalSalesTax
		this.setTotalSalesTax(check.getSalesTax());
	}

	@Override
	public double getTipPercentage() {
		double serverTipPct = this.server.getTargetTipPct();
		return serverTipPct;
	}
}