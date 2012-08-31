
package propertybuilder.application.gui;

import java.awt.Component;
import javax.swing.DefaultListCellRenderer;
import javax.swing.JList;
import propertybuilder.pattern.Variable;

/**
 *
 * @author Ciprian
 */
public class VariableJList extends JList {

    public VariableJList() {
        super();
        this.setCellRenderer( new VariableListCellRenderer() );
    }

    public VariableJList( String[] data ) {
        super( data );
        this.setCellRenderer( new VariableListCellRenderer() );
    }

    private class VariableListCellRenderer extends DefaultListCellRenderer {

        public VariableListCellRenderer() {
            super();
        }

        @Override
        public Component getListCellRendererComponent( JList list, Object value, int index, boolean isSelected, boolean cellHasFocus ) {
            if( value instanceof Variable ) {
                return super.getListCellRendererComponent( list,
                    ((Variable) value).getName(), index, isSelected, cellHasFocus );
            } else {
                return super.getListCellRendererComponent( list,
                    value, index, isSelected, cellHasFocus );
            }
        }
    }
}
