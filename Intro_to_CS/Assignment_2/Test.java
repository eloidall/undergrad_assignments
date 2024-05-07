
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;

public class Test {

	public static void main(String[] args) {
		Owner Amara = new Owner("Amara");
		Staff Sade = new Staff("Sade", true);
		Server Nia = new Server("Nia", 20);
		Restaurant MamaAfrica = new Restaurant("Mama Africa", 1200, Amara, Sade, Nia);

		int total = 0;
		int ptr = 0;
		//check Restaurant
		try{
			total += Restaurant_check01(MamaAfrica, Amara,Sade,Nia);
			System.out.println(total+"/4");
			System.out.println("-------------------End--------------------\n");

			ptr = Restaurant_check02(MamaAfrica, Amara,Sade,Nia);
			total += ptr;
			System.out.println(ptr+"/8");
			System.out.println("-------------------End--------------------\n");

			ptr = Restaurant_check03(MamaAfrica, Amara,Sade,Nia);
			total += ptr;
			System.out.println(ptr+"/6");
			System.out.println("-------------------End--------------------\n");

		}catch (Exception e){
			System.out.println("Something went wrong. Object initialization failed.");
		}

		WorkingOwner tom = new WorkingOwner("Tom", 10);
		FoodStand fs = new FoodStand("FoodStand", 100.0 , tom);

		try{
			ptr = Foodstand_check01(tom, fs);
			total += ptr;
			System.out.println(ptr+"/6");
			System.out.println("-------------------End--------------------\n");

		}catch (Exception e){
			System.out.println("Something went wrong. Object initialization failed.");
		}

		try{
			ptr = Fastfood_check01();
			total += ptr;
			System.out.println(ptr+"/12");
			System.out.println("-------------------End--------------------\n");
		}catch (Exception e){
			System.out.println("Something went wrong..");
		}

		try{
			ptr= IncomeTaxPayer_check();
			total += ptr;
			System.out.println(ptr+"/2");
			System.out.println("-------------------End--------------------\n");

			ptr= Staff_check01();
			total += ptr;
			System.out.println(ptr+"/6");
			System.out.println("-------------------End--------------------\n");

			ptr= checkServer();
			total += ptr;
			System.out.println(ptr+"/2");
			System.out.println("-------------------End--------------------\n");

			ptr= checkOwner();
			total += ptr;
			System.out.println(ptr+"/4");
			System.out.println("-------------------End--------------------\n");

			ptr= checkCheck();
			total += ptr;
			System.out.println(ptr+"/2");
			System.out.println("-------------------End--------------------\n");

			ptr= checkCustomer();
			total += ptr;
			System.out.println(ptr+"/4");
			System.out.println("-------------------End--------------------\n");

			ptr= checkTaxCollector();
			total += ptr;
			System.out.println(ptr+"/4");
			System.out.println("-------------------End--------------------\n");
			System.out.println(total+"/60");




		}catch (Exception e){
			System.out.println("Something went wrong. Object initialization failed.");
		}

	}

	public static int Restaurant_check01(Restaurant MamaAfrica, Owner Amara, Staff Sade,Server Nia) {
		int points = 0;
		//Restaurant Constructor test
		//Check Restaurant's Fixed cost
		if(MamaAfrica.getFixedCosts()==1200){
			System.out.println("Restaurant_check01 Pass01");
			points += 1;
		}else{
			System.out.println("Owner mismatch: owner field not set in Restaurant");
		}

		//Check Restaurant's owner
		if(MamaAfrica.getOwner() == Amara){
			System.out.println("Restaurant_check01 Pass02");
			points += 1;
		}else{
			System.out.println("Owner mismatch: owner field not set in Restaurant");
		}

		//Check Restaurant's Cook
		if(MamaAfrica.getCook() == Sade){
			System.out.println("Restaurant_check01 Pass03");
			points += 1;
		}else{
			System.out.println("Cook mismatch: cook field not set in Restaurant");
		}

		//Check Restaurant's Cook
		if(MamaAfrica.getServer() == Nia){
			System.out.println("Restaurant_check01 Pass04");
			points += 1;
		}else{
			System.out.println("Server mismatch: server field not set in Restaurant");
		}

		return points;
	}

	//Check workShift getIncomeTaxPayers
	public static int Restaurant_check02(Restaurant MamaAfrica, Owner Amara, Staff Sade,Server Nia){
		int points = 0;
		MamaAfrica.workShift(8);

		if(240==Amara.getSalaryExpenses()){
			System.out.println("Restaurant_check02 Pass01");
			points+=2;
		}else{
			System.out.println("Income mismatch: check your getSalaryExpenses.");
		}

		if(160==Sade.getIncome()){
			System.out.println("Restaurant_check02 Pass02");
			points+=1;
		}else{
			System.out.println("Income mismatch: check your cook income");
		}

		if(80==Nia.getIncome()){
			System.out.println("Restaurant_check02 Pass03");
			points+=1;
		}else{
			System.out.println("Income mismatch: check your server income");
		}

		//getIncomeTaxPayers:
		List<IncomeTaxPayer> payers = new ArrayList<IncomeTaxPayer>();
		payers.add(Sade);
		payers.add(Amara);
		payers.add(Nia);
		boolean result = new HashSet<>(payers).equals(new HashSet<>(MamaAfrica.getIncomeTaxPayers()));
		if(result){
			System.out.println("Restaurant_check02 Pass04");
			points+=4;
		}else{
			System.out.println("getIncomeTaxPayers not returning all employees.");
		}
		return points;
	}

	public static int Restaurant_check03(Restaurant MamaAfrica, Owner Amara, Staff Sade,Server Nia){
		int points = 0;
		MamaAfrica.getServer().getIncome();
		//Distribute income and sales tax
		Check check = new Check(180);
		check.setTipByPct(20);
		MamaAfrica.distributeIncomeAndSalesTax(check);

		double ownerIncome = MamaAfrica.getOwner().getIncome();
		if(ownerIncome==180){
			System.out.println("Restaurant_check03 Pass01");
			points+=1;
		}else{
			System.out.println("distributeIncomeAndSalesTax failed. Did you implement check's constructor?");
		}

		double serverIncome = MamaAfrica.getServer().getIncome();
		if(serverIncome==108.8){
			System.out.println("Restaurant_check03 Pass02");
			points+=1;
		}else{
			System.out.println("distributeIncomeAndSalesTax failed. Server distribution failed. ");
		}


		double cookIncome = MamaAfrica.getCook().getIncome();
		if(cookIncome==167.2){
			System.out.println("Restaurant_check03 Pass03");
			points+=1;
		}else{
			System.out.println("distributeIncomeAndSalesTax failed. Cook distribution failed. ");
		}

		double salesTax = MamaAfrica.getTotalSalesTax();
		if(salesTax==27){
			System.out.println("Restaurant_check03 Pass04");
			points+=1;
		}else{
			System.out.println("salesTax failed. distributeIncomeAndSalesTax failed on gettotalsalestax. ");
		}


		int serverTip = MamaAfrica.getServer().getTargetTipPct();
		if(serverTip==20){
			System.out.println("Restaurant_check03 Pass05");
			points+=2;
		}else{
			System.out.println("getTipPercentageTest failed. ");
		}
		return points;
	}

	public static int Foodstand_check01(WorkingOwner tom, FoodStand fs ){
		int points = 0;
		List<IncomeTaxPayer> owners = fs.getIncomeTaxPayers();
		if(1==owners.size()){
			System.out.println("Foodstand_check01 Pass01");
			points+=1;
		}else{
			System.out.println("Foodstand should have only one owner");
		}

		if(tom==owners.get(0)){
			System.out.println("Foodstand_check01 Pass02");
			points+=1;
		}else{
			System.out.println("The owner should be an Workingowner.");
		}

		Check check = new Check(180.0);
		check.setTipByPct(20);
		fs.distributeIncomeAndSalesTax(check);
		if(216==tom.getIncome()){
			System.out.println("Foodstand_check01 Pass03");
			points+=2;
		}else{
			System.out.println("Distributeincomeandsalestax failed.");
		}


		if(10==fs.getTipPercentage()){
			System.out.println("Foodstand_check01 Pass04");
			points+=2;
		}else{
			System.out.println("Foodstand.getTipPercentage() failed.");
		}
		return points;
	}

	public static int Fastfood_check01(){
		Owner Ricardo = new Owner("Ricardo");
		Staff Andrew = new Staff("Andrew", false);
		Staff Alphonse = new Staff("Alphonse", false);
		Staff Rissah = new Staff("Rissah", true);
		Staff Yung = new Staff("Yung", false);
		List<Staff> staff = new ArrayList<Staff>();
		staff.add(Andrew);
		staff.add(Alphonse);
		staff.add(Rissah);
		staff.add(Yung);

		FastFood McDonald = new FastFood("McDonald", 730, Ricardo, staff);

		int points = 0;
		//Check constructor fields
		if(McDonald.getName().equals("McDonald")){
			System.out.println("Fastfood_check01 Pass01");
			points+=1;
		}else{
			System.out.println("Fastfood constructor test failed: Name not set.");
		}
		if(McDonald.getFixedCosts()==730){
			System.out.println("Fastfood_check01 Pass02");
			points+=1;
		}else{
			System.out.println("Fastfood constructor test failed: Fixedcosts not set.");
		}
		// if(McDonald.getOwner()==Ricardo){
		// 	System.out.println("Fastfood_check01 Pass03");
		// 	points+=1;
		// }else{
		// 	System.out.println("Fastfood constructor test failed: Owner not set.");
		// }
		// if(McDonald.getOwner()==Ricardo){
		// 	System.out.println("Fastfood_check01 Pass04");
		// 	points+=1;
		// }else{
		// 	System.out.println("Fastfood constructor test failed: Owner not set.");
		// }
		//shallow copy test
		if(!(McDonald.getStaff()==staff)){
			System.out.println("Fastfood_check01 Pass05");
			points+=2;
		}else{
			System.out.println("Fastfood staff failed. You should do a shallow copy.");
		}

		//check owner's expense
		McDonald.workShift(8);
		if (Ricardo.getSalaryExpenses()==400){
			System.out.println("Fastfood_check01 Pass06");
			points+=2;
		}else{
			System.out.println("workShift() in Fastfood failed. ");
		}

		//check staff's income
		if (Andrew.getIncome()==80 && Rissah.getIncome()==160){
			System.out.println("Fastfood_check01 Pass07");
			points+=2;
		}else{
			System.out.println("workShift() in Fastfood failed: Check the income distribution to each staff ");
		}

		//check getIncomeTaxPayers
		List<IncomeTaxPayer> payers1 = new ArrayList<IncomeTaxPayer>();
		payers1.add(Andrew);
		payers1.add(Yung);
		payers1.add(Rissah);
		payers1.add(Ricardo);
		payers1.add(Alphonse);
		boolean result = new HashSet<>(payers1).equals(new HashSet<>(McDonald.getIncomeTaxPayers()));
		if (result){
			System.out.println("Fastfood_check01 Pass08");
			points+=2;
		}else{
			System.out.println("getIncomeTaxPayers() in Fastfood failed: Check if the owner and all staff are returned.");
		}


		Check check = new Check(180.0);
		check.setTipByPct(20);

		McDonald.distributeIncomeAndSalesTax(check);
		if(180 ==  Ricardo.getIncome() && 89==Yung.getIncome()){
			System.out.println("Fastfood_check01 Pass09");
			points+=2;
		}else{
			System.out.println("distributeIncomeAndSalesTax() in Fastfood failed");
		}
		return points;

	}

	public static int IncomeTaxPayer_check(){
		//checks equals
		int points = 0;
		Staff Sade = new Staff("Sade", false);
		Staff Jude = new Staff("Sade", false);

		if(!(Sade.getTaxID()==Jude.getTaxID())){
			System.out.println("IncomeTaxPayer_check Pass01");
			points+=2;
		}else{
			System.out.println("IncomeTaxPayer equals() test failed.");
		}
		return points;
	}

	public static int Staff_check01(){
		Staff ann = new Staff("Ann", true);
		Staff tina = new Staff("Tina", false);
		int points = 0;

		if(20==ann.getSalaryPerHour() && 10==tina.getSalaryPerHour()){
			System.out.println("IncomeTaxPayer_check Pass02");
			points+=2;
		}else{
			System.out.println("check the iscook field in Staff constructor");
		}

		if (ann.workHours(8)==160){
			System.out.println("IncomeTaxPayer_check Pass03");
			points+=2;
		}else{
			System.out.println("check the return value in workHours()");
		}

		//check incometax/
		ann.workHours(8);
		if (ann.calculateIncomeTax()==80){
			System.out.println("IncomeTaxPayer_check Pass04");
			points+=2;
		}else{
			System.out.println("check calculateIncomeTax()");
		}

		return points;

	}



	public static int checkServer(){

		Server tod = new Server("Tod", 15);
		int points = 0;
		if (10 == tod.getSalaryPerHour()){
			System.out.println("CheckServer Pass01");
			points+=2;
		}else{
			System.out.println("check the return value in getSalaryPerHour()");
		}
		return points;

	}

	//
	public static int checkOwner(){
		Owner Ricardo = new Owner("Ricardo");
		Staff Andrew = new Staff("Andrew", false);
		Staff Alphonse = new Staff("Alphonse", false);
		List<Staff> staff = new ArrayList<Staff>();
		staff.add(Andrew);
		staff.add(Alphonse);

		FastFood McDonald = new FastFood("McDonald", 230, Ricardo, staff);
		Check check = new Check(480.0);
		check.setTipByPct(20);
		McDonald.workShift(8);
		McDonald.distributeIncomeAndSalesTax(check);
		double tax = Ricardo.calculateIncomeTax();
		int points = 0 ;
		if (9.0 == tax){
			System.out.println("checkOwner Pass01");
			points += 4;
		}else{
			System.out.println("Fail. Check the return value of calculateIncomeTax()");
		}
		return points;
	}

	public static int checkCheck(){
		int points = 0;
		Check ch  = new Check(200.0);
		ch.setTipByPct(0.16);
		if (0.32 == ch.getTip()){
			System.out.println("checkCheck Pass01");
			points += 2;
		}else{
			System.out.println("Fail. Check your setTipByPct() again");
		}
		return points;
	}

	public static int checkCustomer(){
		int points = 0;
		Customer tedd = new Customer("Tedd", 12);
		Owner Tina = new Owner("Tina");
		Staff Sade = new Staff("Sade", false);
		Server Nia = new Server("Nia", 20);
		Restaurant MamaAfrica = new Restaurant("Mama Africa", 1200, Tina, Sade, Nia);
		tedd.dineAndPayCheck(MamaAfrica, 200);
		if(30.0 == MamaAfrica.getTotalSalesTax()){
			points += 4;
			System.out.println("checkCustomer Pass01");
		}else{
			System.out.println("Fail. Check your dineAndPayCheck() again.");
		}
		return points;

	}

	public static int checkTaxCollector(){
		Owner Tina = new Owner("Tina");
		Staff Sade = new Staff("Sade", false);
		Server Nia = new Server("Nia", 20);
		Restaurant MamaAfrica = new Restaurant("Mama Africa", 1200, Tina, Sade, Nia);

		WorkingOwner tom = new WorkingOwner("Tom", 10);
		FoodStand fs = new FoodStand("FoodStand", 100.0 , tom);

		Owner Ricardo = new Owner("Ricardo");
		Staff Andrew = new Staff("Andrew", false);
		Staff Alphonse = new Staff("Alphonse", false);
		Staff Rissah = new Staff("Rissah", true);
		Staff Yung = new Staff("Yung", false);
		List<Staff> staff = new ArrayList<Staff>();
		staff.add(Andrew);
		staff.add(Alphonse);
		staff.add(Rissah);
		staff.add(Yung);

		FastFood McDonald = new FastFood("McDonald", 730, Ricardo, staff);

		List<FoodPlace> fpList = new ArrayList<FoodPlace>();
		fpList.add(MamaAfrica);
		fpList.add(McDonald);
		fpList.add(fs);



		TaxCollector tc = new TaxCollector(fpList);

		Check check1 = new Check(300);
		check1.setTipByPct(15);

		Check check2 = new Check(110);
		check1.setTipByPct(18);

		MamaAfrica.workShift(5);
		MamaAfrica.distributeIncomeAndSalesTax(check1);
		McDonald.workShift(8);
		McDonald.distributeIncomeAndSalesTax(check2);
		fs.workShift(4);
		fs.distributeIncomeAndSalesTax(check1);
		tc.collectTax();
		int points = 0 ;
		if(106.5 == tc.getSalesTaxCollected() && 163.9 == tc.getIncomeTaxCollected() ){
			points += 4;
			System.out.println("checkTaxCollector. Pass01");
		}else{
			System.out.println("Fail. Check collectTax() again.");

		}
		return points;
	}


}