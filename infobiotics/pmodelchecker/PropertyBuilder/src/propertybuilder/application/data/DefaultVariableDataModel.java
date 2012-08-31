
package propertybuilder.application.data;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.Iterator;
import javax.swing.ComboBoxModel;
import javax.swing.ListModel;
import javax.swing.event.ListDataListener;
import propertybuilder.pattern.Variable;
import propertybuilder.pattern.VariableType;

/**
 *
 * @author Ciprian
 */
public class DefaultVariableDataModel implements VariableDataModel {

    private Hashtable<VariableType, ArrayList<Variable>> variables;
    private Hashtable<VariableType, ComboBoxModel> varListModels;
    private ComboBoxModel allVarsListModel;
    private ArrayList<Variable> varList;

    public DefaultVariableDataModel() {
        init();
    }

    public void init() {
        variables = new Hashtable<VariableType, ArrayList<Variable>>();
        varList = new ArrayList<Variable>();
        varListModels = new Hashtable<VariableType, ComboBoxModel>();
        allVarsListModel = new VariableListModel();
    }

    public void addVariable( Variable v ) {
        ArrayList<Variable> list = variables.get( v.getType() );
        if( list == null ) {
            list = new ArrayList<Variable>();
            variables.put( v.getType(), list );
        }
        
        list.add( v );
        varList.add( v );
    }

    public void removeVariable( Variable v ) {
        ArrayList<Variable> list = variables.get( v.getType() );
        if( list == null ) {
            return;
        }

        list.remove( v );
        varList.remove( v );
    }

    public Variable getVariable( int index, VariableType type ) {
        ArrayList<Variable> list = variables.get( type );
        if( list == null ) {
            return null;
        }

        return list.get( index );
    }

    public Variable getVariable( String id ) {
        for( Variable v : varList ) {
            if( v.getId().equals( id ) ) {
                return v;
            }
        }

        return null;
    }

    public Variable[] getVariables( VariableType type ) {
        return varList.toArray( new Variable[0] );
    }

    public ComboBoxModel getVariableListModel( VariableType type, boolean create ) {
        if( type == null ) {
            return getVariableListModel();
        }

        ComboBoxModel model = varListModels.get( type );
        if( model == null ) {
            if( create ) {
                model = new VariableListModel( type );
                varListModels.put( type, model );
            }
        }

        return model;
    }

    public ComboBoxModel getVariableListModel( VariableType type ) {
        return getVariableListModel( type, true );
    }

    public ComboBoxModel getVariableListModel() {
        return this.allVarsListModel;
    }

    public ArrayList<Variable> getVariableList( VariableType type ) {
        ArrayList<Variable> list = variables.get( type );
        if( list == null ) {
            list = new ArrayList<Variable>();
            variables.put( type, list );
        }

        return list;
    }

    public VariableType[] getVariableTypes() {
        return variables.keySet().toArray( new VariableType[0] );
    }

    public int getVariableCount() {
        return variables.size();
    }

    public int getVariableCount( VariableType type ) {
        ArrayList<Variable> list = variables.get( type );
        if( list == null ) {
            return 0;
        }

        return list.size();
    }

    @Override
    public String toString() {
        StringBuffer buf = new StringBuffer();
        String lineSep = System.getProperty( "line.separator" );
        buf.append( "Variables: " + lineSep );
        buf.append( "Total: " + getVariableCount() + lineSep );
        Iterator<Variable> it = varList.iterator();
        while( it.hasNext() ) {
            Variable v = it.next();
            buf.append( "[Var ID: " + v.getId() + "; " );
            buf.append( "Name: " + v.getName() + "; " );
            buf.append( "Description: " + v.getDescription() + "]" + lineSep );
        }

        return buf.toString();
    }

    private class VariableListModel implements ComboBoxModel {

        private VariableType varType;
        private ArrayList<Variable> variableList;
        private Variable selectedVar;

        public VariableListModel() {
            this( null );
        }

        public VariableListModel( VariableType type ) {
            varType = type;
            if( type == null ) {
                variableList = DefaultVariableDataModel.this.varList;
            } else {
                variableList = variables.get( varType );
                if( variableList == null ) {
                    variableList = new ArrayList<Variable>();
                    variables.put( varType, variableList );
                }
            }
        }

        public VariableType getVariableType() {
            return this.varType;
        }

        public int getSize() {
            return variableList.size();
        }

        public Object getElementAt( int index ) {
            return variableList.get( index );
        }

        public void addListDataListener( ListDataListener l ) {
            
        }

        public void removeListDataListener( ListDataListener l ) {
            
        }

        public void setSelectedItem( Object anItem ) {
            if( anItem instanceof Variable ) {
                selectedVar = (Variable) anItem;
            }
        }

        public Object getSelectedItem() {
            return selectedVar;
        }
    }
}
