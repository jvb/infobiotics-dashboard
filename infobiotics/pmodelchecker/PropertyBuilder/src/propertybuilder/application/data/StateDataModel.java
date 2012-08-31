
package propertybuilder.application.data;

import javax.swing.ListModel;

/**
 *
 * @author Ciprian
 */
public interface StateDataModel extends ListModel {
    public void addState( State state );
    public void removeState( State state );
    public void removeStates( State[] states );
}
