
package propertybuilder.application;

/**
 *
 * @author Ciprian
 */
public interface CommandExecutor {
    public boolean validCommand( String cmd );
    public String[] getCommands();

    public void execute( String cmd );
    public void execute( String cmd, ArgumentList args );
}
