
package propertybuilder.application;

import java.util.ArrayList;

/**
 *
 * @author Ciprian
 */
public abstract class AbstractCommandExecutor implements CommandExecutor {

    private ArrayList<String> cmdList;

    public AbstractCommandExecutor() {
        cmdList = new ArrayList<String>();
    }

    public void addSupportedCommand( String newCommand ) {
        cmdList.add( newCommand );
    }

    public void removeSupportedCommand( String cmd ) {
        cmdList.remove( cmd );
    }

    public boolean validCommand( String cmd ) {
        return cmdList.contains( cmd );
    }

    public String[] getCommands() {
        return cmdList.toArray( new String[0] );
    }

    public void execute( String cmd ) {
        execute( cmd, null );
    }
}
