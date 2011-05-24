

package propertybuilder.application;

import javax.swing.JComponent;

/**
 *
 * @author Ciprian
 */
public interface VisibleApplicationModule extends ApplicationModule {
    public void setModuleVisible( boolean b );
    public JComponent getGUI();
}
