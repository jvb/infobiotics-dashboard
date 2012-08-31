
package propertybuilder.application.aspects;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.FocusEvent;
import java.awt.event.FocusListener;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.util.EventObject;
import propertybuilder.pattern.InputElement;
import propertybuilder.pattern.Variable;

/**
 *
 * @author Ciprian
 */
public class SymbolSubstituteListener implements
            ActionListener, ItemListener, FocusListener {

        private Variable inputVariable;

        public SymbolSubstituteListener() {
        }

        public void setInputSymbol( Variable inputVariable ) {
            this.inputVariable = inputVariable;
        }

        public Object getInputSymbol() {
            return this.inputVariable;
        }

        private void setValueFromEvent( EventObject e ) {
            if( inputVariable != null ) {
                inputVariable.setValue( ( (InputElement) e.getSource() ).getValue() );
            }
        }

        public void actionPerformed( ActionEvent e ) {
            if ( e.getSource() instanceof InputElement ) {
                setValueFromEvent( e );
            }
        }

        public void itemStateChanged( ItemEvent e ) {
            if ( e.getStateChange() == ItemEvent.SELECTED ) {
                if ( e.getSource() instanceof InputElement ) {
                    setValueFromEvent( e );
                }
            }
        }

        public void focusGained( FocusEvent e ) {
        }

        public void focusLost( FocusEvent e ) {
            if ( e.getSource() instanceof InputElement ) {
                setValueFromEvent( e );
            }
        }
    }

    
