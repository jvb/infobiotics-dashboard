
package propertybuilder.application.modules;

import propertybuilder.application.*;
import java.io.File;
import java.io.IOException;

/**
 *
 * @author Ciprian
 */
public interface ApplicationLog extends ApplicationModule {
    public void update( String msg );
    public void update( String msg, boolean includeDate, boolean includeTime );
    public void clear();
    public void save( File f ) throws IOException;
}
