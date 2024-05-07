
public class Server extends Staff {
	
	private int targetTipPct;

	public Server(String name, int targetTipPct){
		super(name, false);
		this.targetTipPct = targetTipPct;
	}

	public int getTargetTipPct() {
		return targetTipPct;
	}
}