
import java.util.ArrayList;
import java.util.List;

public class FastFood extends FoodPlace {

    private List<Staff> staff = new ArrayList<>();

    public FastFood(String name, double fixedCosts, Owner owner, List<Staff> staff) {
        super(name,fixedCosts,owner);
        List<Staff> shallowCopyStaff = new ArrayList<>();
        for(Staff employee : staff){
            shallowCopyStaff.add(employee);
        }
        this.staff = shallowCopyStaff;
    }

    public List<Staff> getStaff() {
        return staff;
    }

    @Override
    public String toString() {
        StringBuilder builder = new StringBuilder();
        builder.append("Name of FastFood: " + this.getName() +
                "\n" + "Owner: " + this.getOwner());
        int index = 1;
        for (Staff staff: staff) {
            builder.append("\n" + "Staff " + index++ + " : " + staff );
        }
        return builder.toString();
    }

    @Override
    public void workShift(int hours) {
        // Iterate in the staff list and update the Staff and owner's salary expenses
        for (Staff employee: staff){
            employee.workHours(hours);
            this.getOwner().setSalaryExpenses(this.getOwner().getSalaryExpenses()+(hours*employee.getSalaryPerHour()));
        }
    }

    @Override
    public List<IncomeTaxPayer> getIncomeTaxPayers() {
        // To create a list of all the IncomeTaxPayers of the FastFood
        ArrayList<IncomeTaxPayer> IncomeTaxPayersList = new ArrayList<IncomeTaxPayer>();
        IncomeTaxPayersList.add(this.getOwner());
        for (IncomeTaxPayer employee : staff){
            IncomeTaxPayersList.add(employee);
        }
        // To return a shallow copy
        ArrayList<IncomeTaxPayer> shallowCopyIncomeTaxPayersList = new ArrayList<>();
        for(IncomeTaxPayer IncomeTaxPayer : IncomeTaxPayersList) {
            shallowCopyIncomeTaxPayersList.add(IncomeTaxPayer);
        }
        return shallowCopyIncomeTaxPayersList;
    }

    @Override
    public void distributeIncomeAndSalesTax(Check check) {
        // To update the owner's income with the menu price
        this.getOwner().setIncome(this.getOwner().getIncome() + check.getMenuPrice());
        // To distribute the tip equally to all Staff's income
        for (Staff employee: staff){
            employee.setIncome(employee.getIncome() + (check.getTip() / staff.size()));
        }
        // To update the Restaurant totalSalesTax
        this.setTotalSalesTax(check.getSalesTax());
    }

    @Override
    public double getTipPercentage() {
        return 0;
    }
}