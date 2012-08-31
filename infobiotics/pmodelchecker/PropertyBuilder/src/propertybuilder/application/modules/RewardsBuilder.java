

package propertybuilder.application.modules;

import javax.swing.JComponent;
import javax.swing.JPanel;
import propertybuilder.application.AbstractCommandExecutor;
import propertybuilder.application.ApplicationContext;
import propertybuilder.application.ApplicationModule;
import propertybuilder.application.ArgumentList;
import propertybuilder.application.VisibleApplicationModule;

/**
 *
 * @author Ciprian
 */
public class RewardsBuilder extends AbstractCommandExecutor implements VisibleApplicationModule {

    private String name = "Rewards Builder";
    private JComponent gui;

    public RewardsBuilder() {
        gui = new RewardsGUI();
    }

    public void init( ApplicationContext context ) {
        context.getGUI().addModuleComponent( this );
    }

    public void dispose() {

    }

    public String getName() {
        return this.name;
    }

    public JComponent getGUI() {
        return gui;
    }

    public void execute( String cmd, ArgumentList args ) {
        
    }

    public void setModuleVisible( boolean b ) {
        gui.setVisible( b );
    }

    public void onInsert( ApplicationContext context ) {
        
    }

    private class RewardsGUI extends JPanel {

        public RewardsGUI() {
            super();
        }
    }
}
