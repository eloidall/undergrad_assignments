
import java.util.ArrayList;
import java.util.List;

public class FoodStand extends FoodPlace {

    public FoodStand(String name, double fixedCosts, WorkingOwner owner) {
        super(name,fixedCosts,owner);
    }

    @Override
    public String toString() {
        return "Name of FoodStand: " + this.getName() +
                "\n" + "Owner: " + this.getOwner();
    }

    @Override
    public void workShift(int hours) {
        // no salaried workers so do nothing
    }

    @Override
    public List<IncomeTaxPayer> getIncomeTaxPayers() {
        ArrayList<IncomeTaxPayer> IncomeTaxPayersList = new ArrayList<IncomeTaxPayer>(1);
        IncomeTaxPayersList.add(this.getOwner());
        return IncomeTaxPayersList;
    }

    @Override
    public void distributeIncomeAndSalesTax(Check check) {
        // To update the owner's income
        this.getOwner().setIncome(this.getOwner().getIncome() + check.getMenuPrice() + check.getTip());
        // To update the Restaurant totalSalesTax
        this.setTotalSalesTax(check.getSalesTax());
    }

    @Override
    public double getTipPercentage() {
        WorkingOwner workingOwner = (WorkingOwner)this.getOwner();
        double targetTipPct = workingOwner.getTargetTipPct();
        return targetTipPct;
    }
}