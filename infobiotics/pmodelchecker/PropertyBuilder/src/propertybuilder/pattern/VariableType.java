
package propertybuilder.pattern;

/**
 *
 * @author Ciprian
 */
public enum VariableType {
    INT, FLOAT, STATE, PROPERTY, REWARD, UNDEFINED;
    
    public static VariableType fromString( String input ) {

        if( input == null ) {
            return VariableType.UNDEFINED;
        }

        if( input.equals( "int" ) ) {
            return VariableType.INT;
        } else if( input.equals( "state" ) ) {
            return VariableType.STATE;
        } else if( input.equals( "float" ) ) {
            return VariableType.FLOAT;
        }

        return VariableType.UNDEFINED;
    }
}
