
package propertybuilder.application.gui;

import java.awt.Component;
import javax.swing.DefaultListCellRenderer;
import javax.swing.JList;
import propertybuilder.application.data.Constant;

/**
 *
 * @author Ciprian
 */
public class ConstantJList extends JList {

    public ConstantJList() {
        super();
        this.setCellRenderer( new ConstantListCellRenderer() );
    }

    public ConstantJList( String[] data ) {
        super( data );
        this.setCellRenderer( new ConstantListCellRenderer() );
    }

    private class ConstantListCellRenderer extends DefaultListCellRenderer {

        public ConstantListCellRenderer() {
            super();
        }

        @Override
        public Component getListCellRendererComponent( JList list, Object value, int index, boolean isSelected, boolean cellHasFocus ) {
            if( value instanceof Constant ) {
                Constant c = (Constant) value;
                return super.getListCellRendererComponent( list,
                    c.getName() + " : " + c.getValue(), index, isSelected, cellHasFocus );
            } else {
                return super.getListCellRendererComponent( list,
                    value, index, isSelected, cellHasFocus );
            }
        }
    }
}
