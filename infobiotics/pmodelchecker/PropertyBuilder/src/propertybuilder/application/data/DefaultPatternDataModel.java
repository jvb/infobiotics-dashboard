
package propertybuilder.application.data;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.Map.Entry;
import javax.swing.ComboBoxModel;
import javax.swing.ListModel;
import javax.swing.event.ListDataListener;
import propertybuilder.pattern.Pattern;
import propertybuilder.pattern.PatternType;

/**
 *
 * @author Ciprian
 */
public class DefaultPatternDataModel implements PatternDataModel, ListModel {

    private int minCapacity = 20;
    private ArrayList<Pattern> listOfPatterns;
    private ArrayList<String> patternClasses;
    
    private String[] pClasses;
    private Hashtable<String, Pattern[]> data;
    private String selectedPatternClass;
    private Pattern[] selectedPatterns;
    private ComboBoxModel classSelectorModel;
    private PatternType patternType;

    public DefaultPatternDataModel( PatternType pType ) {
        this.patternType = pType;
        init();
    }

    private void init() {
        listOfPatterns = new ArrayList<Pattern>();
        listOfPatterns.ensureCapacity( minCapacity );

        classSelectorModel = new CBModel();
        selectedPatterns = new Pattern[0];
        pClasses = new String[0];
        data = new Hashtable<String, Pattern[]>();
    }

    public void addPattern( Pattern pattern ) {
        listOfPatterns.add( pattern );
    }

    public void removePattern( Pattern pattern ) {
        listOfPatterns.remove( pattern );
    }

    public void updateModel() {
        Hashtable<String, ArrayList<Pattern>> cpMap =
                new Hashtable<String, ArrayList<Pattern>>();
        patternClasses = new ArrayList<String>();
        patternClasses.ensureCapacity( 10 );
        
        for( Pattern p : listOfPatterns ) {
            String pClass = p.getPatternClass();

            if( !patternClasses.contains( pClass ) ) {
                patternClasses.add( pClass );
            }

            ArrayList<Pattern> pList = cpMap.get( pClass );
            if( pList == null ) {
                pList = new ArrayList<Pattern>();
                cpMap.put( pClass, pList );
            }

            pList.add( p );
        }

        data.clear();
        for( Entry<String, ArrayList<Pattern>> entry : cpMap.entrySet() ) {
            data.put( entry.getKey(), entry.getValue().toArray( new Pattern[0] ) );
        }
        pClasses = patternClasses.toArray( new String[0] );
    }

    public void clearModel() {
        this.init();
    }

    public String[] getPatternClasses() {
        return pClasses;
    }

    public Pattern[] getPatterns( String patternClass ) {
        return data.get( patternClass );
    }

    public PatternType getPatternType() {
        return this.patternType;
    }

    public Pattern getPattern( String id ) {
        for( Pattern p : this.listOfPatterns ) {
            if( p.getId().equals( id ) ) {
                return p;
            }
        }

        return null;
    }

    public Pattern[] getPatternsByName( String patternName ) {
        ArrayList<Pattern> pa = new ArrayList<Pattern>();
        for( Pattern p : this.listOfPatterns ) {
            if( p.getName().equalsIgnoreCase( patternName ) ) {
                pa.add( p );
            }
        }

        return pa.toArray( new Pattern[0] );
    }

    public int getPatternCount() {
        return this.listOfPatterns.size();
    }

    public int getSize() {
        return this.selectedPatterns.length;
    }

    public Object getElementAt( int index ) {
        return this.selectedPatterns[index];
    }

    public void addListDataListener( ListDataListener l ) {
        
    }

    public void removeListDataListener( ListDataListener l ) {

    }

    public ComboBoxModel patternClassModel() {
        return this.classSelectorModel;
    }

    public ListModel asListModel() {
        return this;
    }

    public String getSelectedPatternClass() {
        return this.selectedPatternClass;
    }
    
    private class CBModel implements ComboBoxModel {

        public CBModel() {
            
        }

        public void setSelectedItem( Object anItem ) {
            selectedPatternClass = String.valueOf( anItem );
            selectedPatterns = data.get( selectedPatternClass );
        }

        public Object getSelectedItem() {
            return selectedPatternClass;
        }

        public int getSize() {
            return pClasses.length;
        }

        public Object getElementAt( int index ) {
            return pClasses[index];
        }

        public void addListDataListener( ListDataListener l ) {
            
        }

        public void removeListDataListener( ListDataListener l ) {
            
        }
    }
}
