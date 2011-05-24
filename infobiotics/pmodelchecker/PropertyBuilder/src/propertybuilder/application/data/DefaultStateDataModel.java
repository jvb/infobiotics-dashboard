
package propertybuilder.application.data;

import java.util.ArrayList;
import javax.swing.event.ListDataEvent;
import javax.swing.event.ListDataListener;

/**
 *
 * @author Ciprian
 */
public class DefaultStateDataModel implements StateDataModel {
    
    private ArrayList<State> listOfStates;

    public DefaultStateDataModel() {
        listOfStates = new ArrayList<State>();
    }

    public void addState( State state ) {
        listOfStates.add( state );
    }

    public void removeState( State state ) {
        listOfStates.remove( state );
    }

    public void removeStates( State[] states ) {
        for( int i = 0; i < states.length; i++ ) {
            listOfStates.remove( states[i] );
        }
    }

    public int getSize() {
        return listOfStates.size();
    }

    public Object getElementAt( int index ) {
        return listOfStates.get( index );
    }

    public void addListDataListener( ListDataListener l ) {
        
    }

    public void removeListDataListener( ListDataListener l ) {
        
    }
}
