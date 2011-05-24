
package propertybuilder.application.data;

import java.util.ArrayList;
import javax.swing.ComboBoxModel;
import propertybuilder.pattern.Variable;
import propertybuilder.pattern.VariableType;

/**
 *
 * @author Ciprian
 */
public interface VariableDataModel {

    public void addVariable( Variable v );
    public void removeVariable( Variable v );
    public Variable getVariable( String id );
    public Variable[] getVariables( VariableType type );
    public ArrayList<Variable> getVariableList( VariableType type );
    public VariableType[] getVariableTypes();
    public int getVariableCount();
    public int getVariableCount( VariableType type );

    public ComboBoxModel getVariableListModel( VariableType type, boolean create );
    public ComboBoxModel getVariableListModel( VariableType type );
    public ComboBoxModel getVariableListModel();
}
