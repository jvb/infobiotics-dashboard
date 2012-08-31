
package propertybuilder.application;

import propertybuilder.application.ApplicationModule;
import propertybuilder.application.modules.ApplicationLog;
import propertybuilder.application.gui.ApplicationGUI;
import propertybuilder.pattern.Pattern;

/**
 *
 * @author Ciprian
 */
public interface ApplicationContext {

    public ApplicationData getApplicationData();
    public ApplicationUtilities getApplicationUtilities();
    public ApplicationSettings getApplicationSettings();
    public ApplicationLog getLog();
    public ApplicationGUI getGUI();

    public void addApplicationModule( ApplicationModule module );
    public void removeApplicationModule( ApplicationModule module );
    public ApplicationModule getApplicationModule( String name );
    public String[] getApplicationModuleNames();
    public void addContextListener( ContextListener listener );
    public void removeContextListener( ContextListener listener );

    public String getTitle();

    public void deploy();
    public void dispose();
    public void execute( String cmd );
    public void execute( String cmd, ArgumentList args );
    public void execute( String cmd, String moduleName, ArgumentList args );

    public void fireSettingsLoaded();
    public void firePatternsLoaded();
    public void firePatternDataChanged();
    public void firePatternSelected( Pattern p );
}
