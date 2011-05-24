
package propertybuilder.pattern;

import javax.swing.JComponent;
import propertybuilder.application.ApplicationData;
import propertybuilder.application.aspects.SymbolSubstituteListener;

/**
 *
 * @author Ciprian
 */
public interface InputElement {
    public void initElement( ApplicationData data );
    public Object getValue();
    public void setValue( Object value );
    public void restrictTo( VariableType type );
    public VariableType getRestriction();
    public JComponent getComponent();
    void setSubstituteListener( SymbolSubstituteListener l );
    SymbolSubstituteListener getSubstituteListener();
    public void releaseElement();
}
