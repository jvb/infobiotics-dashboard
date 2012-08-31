
package propertybuilder.application;

/**
 *
 * @author Ciprian
 */
public interface ApplicationModule extends CommandExecutor {
    public void onInsert( ApplicationContext context );
    public void init( ApplicationContext context );
    public void dispose();

    public String getName();
}
