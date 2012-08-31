
package propertybuilder.application.modules;

import propertybuilder.application.*;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Calendar;
import javax.swing.BorderFactory;
import javax.swing.JComponent;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;

/**
 *
 * @author Ciprian
 */
public class DefaultApplicationLog extends JTextArea implements ApplicationLog, VisibleApplicationModule {

    private String lineEnd = System.getProperty( "line.separator" );
    private boolean defaultIncludeDate = false;
    private boolean defaultIncludeTime = true;
    private JComponent gui;

    private ArrayList<String> validCommands;

    public DefaultApplicationLog() {
        super();
        gui = new LogGUI();
        validCommands = new ArrayList<String>();
        validCommands.add( "logupdate" );
    }

    public void setIncludeDate( boolean b ) {
        this.defaultIncludeDate = b;
    }

    public boolean isIncludeDateSet() {
        return this.defaultIncludeDate;
    }

    public void setIncludeTime( boolean b ) {
        this.defaultIncludeTime = b;
    }

    public boolean getIncludeTime() {
        return this.defaultIncludeTime;
    }

    public void update( String msg ) {
        this.append( msg );
        this.append( lineEnd );
    }

    public void update( String msg, boolean includeDate, boolean includeTime ) {

        Calendar c = Calendar.getInstance();

        if( includeDate && !includeTime ) {
            this.append( String.format( "%1$td.%1$tm.%1$tY", c ) );
        } else if( includeTime && !includeDate ) {
            this.append( String.format( "%1$tH:%1$tM:%1$tS", c ) );
        } else {
            this.append( String.format( "%1$td.%1$tm.%1$tY %1$tH:%1$tM:%1$tS", c ) );
        }

        this.append( " " + msg + lineEnd );
    }

    public void clear() {
        this.setText( "" );
    }

    public void save( File f ) throws IOException {
        if( !f.exists() ) {
            return;
        }

        BufferedWriter bw = new BufferedWriter( new FileWriter( f ) );
        bw.append( this.getText() );
        bw.close();
    }

    public void init( ApplicationContext context ) {
        if( context.getGUI() != null ) {
            context.getGUI().addModuleComponent( this );
        }
    }

    public void dispose() {
        
    }

    @Override
    public String getName() {
        return "log";
    }

    public boolean hasGUI() {
        return true;
    }

    public JComponent getGUI() {
        return gui;
    }

    public boolean validCommand( String cmd ) {
        return false;
    }

    public String[] getCommands() {
        return null;
    }

    public void execute( String cmd ) {
        
    }

    public void execute( String cmd, ArgumentList args ) {
        
    }

    public void setModuleVisible( boolean b ) {
        gui.setVisible( false );
    }

    public void onInsert( ApplicationContext context ) {
        if( context instanceof DefaultApplicationContext ) {
            ((DefaultApplicationContext) context).setLog( this );
        }
    }

    private class LogGUI extends JScrollPane {

        public LogGUI() {
            super( DefaultApplicationLog.this );
            this.setBorder( BorderFactory.createTitledBorder(
                    BorderFactory.createEtchedBorder(), "Log" ) );
        }
    }
}
