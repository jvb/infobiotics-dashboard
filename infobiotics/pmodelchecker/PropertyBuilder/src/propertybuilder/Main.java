
package propertybuilder;

import java.util.Iterator;
import javax.swing.JScrollPane;
import propertybuilder.application.modules.ApplicationLog;
import propertybuilder.application.ApplicationSettings;
import propertybuilder.application.DefaultApplicationContext;
import propertybuilder.application.modules.DefaultApplicationLog;
import propertybuilder.application.gui.ApplicationGUI;
import propertybuilder.application.modules.PropertyBuilder;
import propertybuilder.application.modules.RewardsBuilder;
import propertybuilder.application.modules.StateBuilder;
import propertybuilder.pattern.Symbol;
import propertybuilder.pattern.SymbolSequence;

/**
 *
 * @author Ciprian
 */
public class Main {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {

        /*
        args = new String[4];
        args[0] = "-paramsFile";
        args[1] = "output.xml";
        args[2] = "-settings";
        args[3] = "output.xml";
        */

        DefaultApplicationContext ctx = new DefaultApplicationContext();
        //first declare all modules and register them in the context
        ApplicationGUI gui = new ApplicationGUI();
        DefaultApplicationLog log = new DefaultApplicationLog();
        RewardsBuilder rbuilder = new RewardsBuilder();
        StateBuilder sbuilder = new StateBuilder();
        PropertyBuilder pbuilder = new PropertyBuilder();


        ctx.addApplicationModule( gui );

        ctx.addApplicationModule( sbuilder );
        ctx.addApplicationModule( rbuilder );
        ctx.addApplicationModule( pbuilder );
        ctx.addApplicationModule( log );

        //now load the application settings
        ApplicationSettings settings = ctx.createApplicationSettings();
        settings.getFromParams( args );

        //and finally deploy context
        ctx.deploy();

        gui.setVisible( true );

        log.update( ctx.getApplicationSettings().toString() );
        log.update( ctx.getApplicationData().variableData.toString() );
    }

//    public static void main( String[] args ) {
//        SymbolSequence ss = new SymbolSequence();
//        ss.parseSequence( "#v3 is Variable #v1 is minimum #v2." );
//        Iterator<Symbol> it = ss.iterator();
//        while( it.hasNext() ) {
//            Symbol x = it.next();
//            System.out.println( x.getSymbolType().toString() + " " +
//                    x.getSymbolName() );
//        }
//    }
}
