
package propertybuilder.application.gui;

import java.awt.Component;
import javax.swing.JList;
import javax.swing.JPanel;
import javax.swing.ListCellRenderer;

/**
 *
 * @author Ciprian
 */
public class PropertyJList extends JList {

    public PropertyJList() {
        super();
    }

    public PropertyJList( String[] data ) {
        super( data );
    }

    private class PropertyListCellRenderer extends JPanel implements ListCellRenderer {

        public Component getListCellRendererComponent( JList list, Object value, int index, boolean isSelected, boolean cellHasFocus ) {
            throw new UnsupportedOperationException( "Not supported yet." );
        }
        
    }
}
