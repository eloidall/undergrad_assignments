
public class WorkingOwner extends Owner {

    private int targetTipPct;

    public WorkingOwner(String name, int targetTipPct) {
        super(name);
        this.targetTipPct = targetTipPct;
    }

    public int getTargetTipPct() {
        return targetTipPct;
    }
}