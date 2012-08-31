

package propertybuilder.application.gui;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Component;
import java.awt.FlowLayout;
import javax.swing.BorderFactory;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.JPanel;
import javax.swing.ListCellRenderer;
import propertybuilder.pattern.Pattern;

/**
 *
 * @author Ciprian
 */
public class PatternJList extends JList {

    public PatternJList() {
        super();
        this.setCellRenderer( new PatternListCellRenderer() );
    }

    public PatternJList( String[] data ) {
        super( data );
        this.setCellRenderer( new PatternListCellRenderer() );
    }

    private class PatternListCellRenderer extends JPanel implements ListCellRenderer {

        private JLabel nameLabel;
        private JLabel descriptionLabel;
        private JLabel questionLabel;
        private JLabel idLabel;
        private JPanel panel;

        private boolean showName;
        private boolean showDescription;
        private boolean showQuestion;
        private boolean showID;

        public PatternListCellRenderer() {
            init();
        }

        private void init() {
            nameLabel = new JLabel();
            descriptionLabel = new JLabel();
            questionLabel = new JLabel();
            idLabel = new JLabel();

            panel = new JPanel( new BorderLayout() );

            JPanel aux = new JPanel( new FlowLayout( FlowLayout.LEADING ) );
            aux.add( idLabel );
            aux.add( nameLabel );
            aux.setOpaque( false );
            panel.add( aux, BorderLayout.NORTH );
            panel.add( questionLabel, BorderLayout.CENTER );
        }

        public void setNameVisible( boolean b ) {
            this.showName = b;
        }

        public boolean isNameVisible() {
            return this.showName;
        }

        public void setDescriptionVisible( boolean b ) {
            this.showName = b;
        }

        public boolean isDescriptionVisible() {
            return this.showName;
        }

        public void setQuestionVisible( boolean b ) {
            this.showQuestion = b;
        }

        public boolean isQuestionVisible() {
            return showQuestion;
        }

        public void setIDVisible( boolean b ) {
            this.showID = b;
        }

        public boolean isIDVisible() {
            return showID;
        }

        public Component getListCellRendererComponent( JList list, Object value, int index, boolean isSelected, boolean cellHasFocus ) {
            if( value instanceof Pattern ) {
                Pattern p = (Pattern) value;
                idLabel.setText( "[" + p.getId() + "]" );
                nameLabel.setText( p.getName() );
                questionLabel.setText( p.getQuestion() );
                descriptionLabel.setText( p.getDescription() );

                if( isSelected ) {
                    panel.setBackground( list.getSelectionBackground() );
                    panel.setForeground( list.getSelectionForeground() );
                    panel.setBorder( BorderFactory.createLineBorder( new Color( 38, 88, 138 ) ) );
                } else {
                    panel.setBackground( list.getBackground() );
                    panel.setForeground( list.getForeground() );
                    panel.setBorder( BorderFactory.createLineBorder( Color.LIGHT_GRAY ) );
                }
            }

            return this.panel;
        }

    }

}
