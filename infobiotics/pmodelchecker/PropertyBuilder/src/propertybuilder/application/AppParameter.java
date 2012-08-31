
package propertybuilder.application;

import java.util.regex.Pattern;

/**
 *
 * @author Ciprian
 */
public class AppParameter {

    private String command;
    private String value;
    private boolean expectValue;
    private boolean found;

    public AppParameter( String command ) {
        setCommand( command );
        //do not expect a value by default; this means that simple presence of
        //the command in the application call is significant for the execution
        //(acts as a program parameter)
        setExpectValue( false );
    }

    public AppParameter( String command, boolean expectValue ) {
        setCommand( command );
        setExpectValue( expectValue );
    }

    public void setCommand( String command ) {
        this.command = command;
    }

    public void setValue( String value ) {
        this.value = value;
    }

    public String getValue() {
        return this.value;
    }

    public String getCommand() {
        return this.command;
    }

    public void setExpectValue( boolean b ) {
        this.expectValue = b;
    }

    public boolean isExpectValue() {
        return this.expectValue;
    }

    public boolean isFound() {
        return this.found;
    }

    public Pattern getCompiledPattern() {
        return Pattern.compile( command );
    }

    public void processParameter( String[] args ) {
        if( args == null ) {
            return;
        }

        for( int i = 0; i < args.length; i++ ) {
            if( args[i].equals( command ) ) {
                this.found = true;
                if( this.expectValue ) {
                    this.value = args[++i];
                }
                
                break;
            }
        }
    }
}
