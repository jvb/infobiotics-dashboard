
package propertybuilder.pattern;

/**
 *
 * @author Ciprian
 */
public class Variable extends Symbol implements IVariable {

    private VariableType type;
    private String initValue;
    private String id;
    private String description;
    private Object value;

    public Variable() {
        this( "undefined", "", "" );
    }

    public Variable( String id ) {
        this( id, id, "" );
    }

    public Variable( String id, String name, String description ) {
        this( id, name, null, description );
    }

    public Variable( String id, String name, String type, String description ) {
        super( SymbolType.VARIABLE );
        setId( id );
        setName( name );
        setType( type );
        setDescription( description );
    }

    public void setId( String id ) {
        this.id = id;
    }

    public String getId() {
        return this.id;
    }

    public void setInitValue( String initValue ) {
        this.initValue = initValue;
    }

    public String getInitValue() {
        return this.initValue;
    }

    public void setType( String type ) {
        this.type = VariableType.fromString( type );
    }

    public VariableType getType() {
        return this.type;
    }

    public void setName( String name ) {
        setSymbolName( name );
    }

    public String getName() {
        return getSymbolName();
    }

    public void setDescription( String description ) {
        this.description = description;
    }

    public String getDescription() {
        return this.description;
    }

    public void setValue( Object value ) {
        this.value = value;
    }

    public String getValue() {
        if( this.value instanceof IVariable ) {
            return ((IVariable) this.value).getValue();
        }

        return this.value.toString();
    }
}
