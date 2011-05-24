
package propertybuilder.application.gui;

import java.awt.Component;
import javax.swing.JList;
import javax.swing.JPanel;
import javax.swing.ListCellRenderer;
import propertybuilder.application.data.StateDataModel;

/**
 *
 * @author Ciprian
 */
public class StateJList extends JList {

    public StateJList( StateDataModel model ) {
        super( model );
    }

    public StateJList( String[] data ) {
        super( data );
    }

    public class StateListCellRenderer extends JPanel implements ListCellRenderer {

        public Component getListCellRendererComponent( JList list, Object value, int index, boolean isSelected, boolean cellHasFocus ) {
            throw new UnsupportedOperationException( "Not supported yet." );
        }
    }

}
