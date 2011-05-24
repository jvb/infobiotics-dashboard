
package propertybuilder.application;

import propertybuilder.application.aspects.SymbolSubstituteFactory;

/**
 *
 * @author Ciprian
 */
public class ApplicationUtilities {

    private ApplicationContext ctx;
    public SymbolSubstituteFactory ssFactory;

    public ApplicationUtilities( ApplicationContext context ) {
        if( context == null ) {
            throw new NullPointerException( "Context must not be null!" );
        } else {
            setApplicationContext( context );
            init();
        }
    }

    private void setApplicationContext( ApplicationContext context ) {
        ctx = context;
    }

    public ApplicationContext getApplicationContext() {
        return this.ctx;
    }

    public void init() {
        ssFactory = new SymbolSubstituteFactory(ctx.getApplicationData());
        ssFactory.setApplicationContext( ctx );
    }
}
