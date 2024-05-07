
import java.util.ArrayList;
import java.util.List;

public class TaxCollector {

	private List<FoodPlace> foodPlaces = new ArrayList<>();
	private double incomeTaxCollected;
	private double salesTaxCollected;

	public TaxCollector(List<FoodPlace> foodPlaces) {
		this.foodPlaces = foodPlaces;
	}

	public List<FoodPlace> getFoodPlaces() {
		return foodPlaces;
	}

	public double getIncomeTaxCollected() {
		return incomeTaxCollected;
	}

	public double getSalesTaxCollected() {
		return salesTaxCollected;
	}

	public void collectTax() {
		salesTaxCollected = 0;
		incomeTaxCollected = 0;
		// To update the salesTaxCollected of every FoodPlace
		for (FoodPlace foodPlace : foodPlaces){
			salesTaxCollected += foodPlace.getTotalSalesTax();
			// To update the incomeTaxCollected of every IncomeTaxPayers
			for (IncomeTaxPayer incomeTaxPayer : foodPlace.getIncomeTaxPayers()){
				incomeTaxCollected += incomeTaxPayer.calculateIncomeTax();
			}
		}
	}
	
	public String toString() {
		return "TaxCollector: income tax collected: " + incomeTaxCollected + ", sales tax collected: " + salesTaxCollected;
	}
}