
package propertybuilder.application;

import propertybuilder.pattern.Pattern;

/**
 *
 * @author Ciprian
 */
public interface ContextListener {
    public void settingsLoaded();
    public void patternsLoaded();
    public void patternDataChanged();
    public void patternSelected( Pattern p );
}
