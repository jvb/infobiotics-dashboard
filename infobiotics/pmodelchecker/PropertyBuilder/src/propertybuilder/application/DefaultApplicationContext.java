
package propertybuilder.application;

import propertybuilder.application.modules.ApplicationLog;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Hashtable;
import java.util.Iterator;
import propertybuilder.application.gui.ApplicationGUI;
import propertybuilder.pattern.Pattern;

/**
 *
 * @author Ciprian
 */
public class DefaultApplicationContext implements ApplicationContext {
    
    private ApplicationData data;
    private ApplicationUtilities utils;
    private ApplicationSettings settings;
    private ArrayList<ApplicationModule> appModules;
    private HashMap<String, ApplicationModule> appModulesTable;
    private CommandExecutor cmd;

    private ArrayList<ContextListener> contextListeners;
    private ApplicationLog log;
    private ApplicationGUI gui;
    private String title = "Property Builder v 1.1";

    public DefaultApplicationContext() {
        init();
        
        setApplicationSettings( new ApplicationSettings( this ) );
        setApplicationData( new ApplicationData( this ) );
        setApplicationUtilities( new ApplicationUtilities( this ) );
    }

    public DefaultApplicationContext( ApplicationSettings settings, ApplicationData data ) {
        init();
        
        this.setApplicationSettings( settings );
        this.setApplicationData( data );
    }

    public void init() {
        contextListeners = new ArrayList<ContextListener>();
        appModules = new ArrayList<ApplicationModule>();
        appModulesTable = new HashMap<String, ApplicationModule>();
        cmd = new ContextCommandExecutor();
    }

    public ApplicationSettings createApplicationSettings() {
        setApplicationSettings( new ApplicationSettings( this ) );
        return this.settings;
    }

    public void setApplicationSettings( ApplicationSettings settings ) {
        this.settings = settings;
    }

    public ApplicationData createApplicationData() {
        setApplicationData( new ApplicationData( this ) );
        return this.data;
    }

    public void setApplicationData( ApplicationData data ) {
        this.data = data;
    }

    public ApplicationUtilities getApplicationUtilities() {
        return this.utils;
    }

    public void setApplicationUtilities( ApplicationUtilities utils ) {
        this.utils = utils;
    }

    public ApplicationData getApplicationData() {
        return this.data;
    }

    public ApplicationSettings getApplicationSettings() {
        return this.settings;
    }

    public void addContextListener( ContextListener listener ) {
        contextListeners.add( listener );
    }

    public void removeContextListener( ContextListener listener ) {
        contextListeners.remove( listener );
    }

    public ApplicationLog getLog() {
        return this.log;
    }

    public void setLog( ApplicationLog log ) {
        this.log = log;
    }

    public String getTitle() {
        return this.title;
    }

    public ApplicationGUI getGUI() {
        return this.gui;
    }

    public void setApplicationGUI( ApplicationGUI gui ) {
        this.gui = gui;
    }

    public void addApplicationModule( ApplicationModule module ) {
        if( !appModules.contains( module ) ) {
            appModules.add( module );
            appModulesTable.put( module.getName(), module );
            module.onInsert( this );
        }
    }

    public void removeApplicationModule( ApplicationModule module ) {
        appModules.remove( module );
        appModulesTable.remove( module.getName() );

        if( gui != null ) {
            if( module instanceof VisibleApplicationModule ) {
                gui.removeModuleComponent( module );
            }
        }
    }

    public ApplicationModule getApplicationModule( String name ) {
        return appModulesTable.get( name );
    }

    public String[] getApplicationModuleNames() {
        return appModulesTable.keySet().toArray( new String[0] );
    }

    public void deploy() {
        Iterator<ApplicationModule> it = appModules.iterator();
        while( it.hasNext() ) {
            it.next().init( this );
        }
    }

    public void dispose() {
        Iterator<ApplicationModule> it = appModules.iterator();
        while( it.hasNext() ) {
            it.next().dispose();
        }
    }

    public void execute( String cmd ) {
        this.execute( cmd, null );
    }

    public void execute( String cmd, ArgumentList args ) {
        this.cmd.execute( cmd, args );
    }

    public void execute( String cmd, String moduleName, ArgumentList args ) {
        ApplicationModule m = appModulesTable.get( moduleName );
        if( m != null ) {
            
        }
    }

    // <editor-fold defaultstate="collapsed" desc="FireEvent methods">
    public void fireSettingsLoaded() {
        for( ContextListener cl : this.contextListeners ) {
            cl.settingsLoaded();
        }
    }

    public void firePatternsLoaded() {
        for( ContextListener cl : this.contextListeners ) {
            cl.patternsLoaded();
        }
    }

    public void firePatternDataChanged() {
        for( ContextListener cl : this.contextListeners ) {
            cl.patternDataChanged();
        }
    }

    public void firePatternSelected( Pattern p ) {
        for( ContextListener cl : this.contextListeners ) {
            cl.patternSelected( p );
        }
    }
    //</editor-fold>

    private class ContextCommandExecutor extends AbstractCommandExecutor {

        public ContextCommandExecutor() {
            super();
            this.addSupportedCommand( "exit" );
        }

        public void execute( String cmd, ArgumentList args ) {
            if( cmd.equals( "exit" ) ) {
                dispose();
                System.exit( 0 );
            } else if( cmd.equals( "" ) ) {
                
            }
        }  
    }
}
