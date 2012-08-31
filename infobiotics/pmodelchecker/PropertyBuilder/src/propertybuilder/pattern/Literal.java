package propertybuilder.pattern;

/**
 * 
 * @author Ciprian
 */
public class Literal extends Symbol {

	private String value;

	public Literal() {
		this("");
	}

	public Literal(String value) {
		super(SymbolType.LITERAL);
		setValue(value);
	}

	public void setValue(String value) {
		this.value = value;
		this.setSymbolName(value);
	}

	public String getValue() {
		return this.value;
	}
}
