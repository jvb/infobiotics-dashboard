
package propertybuilder.application.data;

import propertybuilder.pattern.VariableType;

/**
 *
 * @author Ciprian
 */
public class Constant {
    private String id;
    //name must be unique
    private String name;
    private String value;
    private VariableType type;
    private String description;

    public Constant() {
        this( "undefined", VariableType.UNDEFINED );
    }

    public Constant( String id, String name, String cType, String description ) {
        setId( id );
        setName( name );
        setType( cType );
        setDescription( description );
    }

    public Constant( String name, VariableType type ) {
        setName( name );
        setType( type );
    }

    public void setId( String id ) {
        this.id = id;
    }

    public String getId() {
        return this.id;
    }

    public void setName( String name ) {
        this.name = name;
    }

    public String getName() {
        return this.name;
    }

    public void setValue( String value ) {
        this.value = value;
    }

    public String getValue() {
        return this.value;
    }

    public void setType( VariableType type ) {
        this.type = type;
    }

    public void setType( String type ) {
        this.type = VariableType.fromString( type );
    }

    public VariableType getType() {
        return this.type;
    }

    public void setDescription( String description ) {
        this.description = description;
    }

    public String getDescription() {
        return this.description;
    }
}
