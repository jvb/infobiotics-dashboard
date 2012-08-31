
package propertybuilder.application;

import java.util.Hashtable;

/**
 *
 * @author Ciprian
 */
public class ArgumentList {
    private Hashtable<String, Object> args;

    public ArgumentList() {
        args = new Hashtable<String, Object>();
    }
    
    public ArgumentList( Object... arguments ) {
        args = new Hashtable<String, Object>();
        if( arguments != null && arguments.length % 2 == 0 ) {
            for( int i = 0; i < arguments.length; i += 2 ) {
                args.put( arguments[i].toString(), arguments[i+1] );
            }
        }
    }

    public Object getArg( String name ) {
        return args.get( name );
    }

    public void setArg( String name, String value ) {
        args.put( name, value );
    }
}
