
package propertybuilder.application.data;

import java.util.ArrayList;
import javax.swing.ComboBoxModel;
import javax.swing.ListModel;
import propertybuilder.pattern.VariableType;

/**
 *
 * @author Ciprian
 */
public interface ConstantDataModel {
    public void addConstant( Constant c );
    public void removeConstant( Constant c );
    public Constant getConstant( String name );
    public Constant[] getConstants( VariableType type );
    public ArrayList<Constant> getConstantList( VariableType type );
    public VariableType[] getConstantTypes();
    public int getConstantCount();
    public int getConstantCount( VariableType type );

    public ComboBoxModel getConstantListModel( VariableType type, boolean create );
    public ComboBoxModel getConstantListModel( VariableType type );
    public ComboBoxModel getConstantListModel();
}
