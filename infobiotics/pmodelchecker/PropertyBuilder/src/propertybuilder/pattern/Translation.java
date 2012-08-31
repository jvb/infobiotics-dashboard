package propertybuilder.pattern;

/**
 * 
 * @author Ciprian
 */
public class Translation {

	private SymbolSequence sequence;
	private String targetSpec;
	private String description;

	public Translation() {
		this("none");
	}

	public Translation(String targetSpec) {
		setTargetSpec(targetSpec);
		sequence = new SymbolSequence();
	}

	public Translation(String targetSpec, String description,
			String sequenceValue) {
		setTargetSpec(targetSpec);
		setDescription(description);
		sequence = new SymbolSequence();
		setSequence(sequenceValue);
	}

	public void setTargetSpec(String targetSpec) {
		this.targetSpec = targetSpec;
	}

	public String getTargetSpec() {
		return this.targetSpec;
	}

	public void setDescription(String description) {
		this.description = description;
	}

	public String getDescription() {
		return this.description;
	}

	public void setSequence(String sequenceValue) {
		sequence.parseSequence(sequenceValue);
	}

	public SymbolSequence getSequence() {
		return this.sequence;
	}
}
