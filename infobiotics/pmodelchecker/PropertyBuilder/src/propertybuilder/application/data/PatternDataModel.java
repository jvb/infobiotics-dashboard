
package propertybuilder.application.data;

import javax.swing.ComboBoxModel;
import javax.swing.ListModel;
import org.w3c.dom.Node;
import propertybuilder.pattern.Pattern;
import propertybuilder.pattern.PatternType;

/**
 *
 * @author Ciprian
 */
public interface PatternDataModel {

    public void addPattern( Pattern pattern );
    public void removePattern( Pattern pattern );
    public void updateModel();
    public void clearModel();

    public String[] getPatternClasses();
    public Pattern[] getPatterns( String patternClass );
    public PatternType getPatternType();
    public Pattern getPattern( String id );
    public Pattern[] getPatternsByName( String patternName );
    public int getPatternCount();

    public ListModel asListModel();
    public ComboBoxModel patternClassModel();
}
