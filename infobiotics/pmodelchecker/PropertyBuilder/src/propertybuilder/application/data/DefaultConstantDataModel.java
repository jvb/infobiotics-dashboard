
package propertybuilder.application.data;

import java.util.ArrayList;
import java.util.Hashtable;
import javax.swing.ComboBoxModel;
import javax.swing.ListModel;
import javax.swing.event.ListDataListener;
import propertybuilder.pattern.VariableType;

/**
 *
 * @author Ciprian
 */
public class DefaultConstantDataModel implements ConstantDataModel {

    private Hashtable<VariableType, ArrayList<Constant>> constants;
    private Hashtable<VariableType, ComboBoxModel> constantListModels;
    private ComboBoxModel allConstantsListModel;
    private ArrayList<Constant> listOfConstants;

    public DefaultConstantDataModel() {
        init();
    }

    public void init() {
        constants = new Hashtable<VariableType, ArrayList<Constant>>();
        listOfConstants = new ArrayList<Constant>();
        constantListModels = new Hashtable<VariableType, ComboBoxModel>();
        allConstantsListModel = new ConstantListModel();
    }

    public void addConstant( Constant c ) {
        ArrayList<Constant> list = constants.get( c.getType() );
        if( list == null ) {
            list = new ArrayList<Constant>();
            constants.put( c.getType(), list );
        }
        list.add( c );
        listOfConstants.add( c );
    }

    public void removeConstant( Constant c ) {
        ArrayList<Constant> list = constants.get( c.getType() );
        if( list == null ) {
            return;
        }

        list.remove( c );
        listOfConstants.remove( c );
    }

    public Constant getConstant( String name ) {
        for( Constant c : listOfConstants ) {
            if( c.getName().equals( name ) ) {
                return c;
            }
        }

        return null;
    }

    public Constant[] getConstants( VariableType type ) {
        return listOfConstants.toArray( new Constant[0] );
    }

    public ComboBoxModel getConstantListModel( VariableType type, boolean create ) {
        ComboBoxModel model = constantListModels.get( type );
        if( model == null ) {
            if( create ) {
                model = new ConstantListModel( type );
                constantListModels.put( type, model );
            }
        }

        return model;
    }

    public ComboBoxModel getConstantListModel( VariableType type ) {
        return getConstantListModel( type );
    }

    public ComboBoxModel getConstantListModel() {
        return this.allConstantsListModel;
    }

    public ArrayList<Constant> getConstantList( VariableType type ) {
        ArrayList<Constant> list = constants.get( type );
        if( list == null ) {
            list = new ArrayList<Constant>();
            constants.put( type, list );
        }

        return list;
    }

    public VariableType[] getConstantTypes() {
        return constants.keySet().toArray( new VariableType[0] );
    }

    public int getConstantCount() {
        return constants.size();
    }

    public int getConstantCount( VariableType type ) {
        ArrayList<Constant> list = constants.get( type );
        if( list == null ) {
            return 0;
        }

        return list.size();
    }

    private class ConstantListModel implements ComboBoxModel {

        private VariableType constantType;
        private ArrayList<Constant> constantList;
        private Constant selectedConstant;

        public ConstantListModel() {
            this( null );
        }

        public ConstantListModel( VariableType type ) {
            constantType = type;
            if( constantType == null ) {
                constantList = DefaultConstantDataModel.this.listOfConstants;
            } else {
                constantList = constants.get( constantType );
                if( constantList == null ) {
                    constantList = new ArrayList<Constant>();
                    constants.put( type, constantList );
                }
            }
        }

        public void setSelectedItem( Object anItem ) {
            if( anItem instanceof Constant ) {
                selectedConstant = (Constant) anItem;
            }
        }

        public Object getSelectedItem() {
            return selectedConstant;
        }

        public int getSize() {
            return constantList.size();
        }

        public Object getElementAt( int index ) {
            return constantList.get( index );
        }

        public void addListDataListener( ListDataListener l ) {
            
        }

        public void removeListDataListener( ListDataListener l ) {
            
        }
    }
}
