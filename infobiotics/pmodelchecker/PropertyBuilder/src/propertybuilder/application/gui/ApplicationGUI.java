

package propertybuilder.application.gui;

import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.util.ArrayList;
import java.util.Hashtable;
import javax.swing.JComponent;
import javax.swing.JFrame;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JTabbedPane;
import propertybuilder.application.AbstractCommandExecutor;
import propertybuilder.application.ApplicationContext;
import propertybuilder.application.ApplicationModule;
import propertybuilder.application.ArgumentList;
import propertybuilder.application.DefaultApplicationContext;
import propertybuilder.application.VisibleApplicationModule;

/**
 *
 * @author Ciprian
 */
public class ApplicationGUI extends AbstractCommandExecutor implements ApplicationModule {

    private JFrame frame;
    private JTabbedPane primaryModuleDisplay;
    private Hashtable<ApplicationModule, Integer> applicationTabIndex;
    private ApplicationContext context;
    private JMenuBar menuBar;
    private Hashtable<String, JMenuItem> menus;

    public ApplicationGUI() {

        frame = new JFrame();
        frame.setSize( 1024, 768 );
        frame.setLocationRelativeTo( null );
        frame.addWindowListener( new WindowAdapter() {
            @Override
            public void windowClosing( WindowEvent event ) {
                context.execute( "exit" );
            }
        });

        primaryModuleDisplay = new JTabbedPane();
        applicationTabIndex = new Hashtable<ApplicationModule, Integer>();
        frame.getContentPane().add( primaryModuleDisplay );

        menuBar = new JMenuBar();
        frame.setJMenuBar( menuBar );
        menus = new Hashtable<String, JMenuItem>();
    }

    public void init( ApplicationContext context ) {
        frame.setTitle( context.getTitle() );
    }

    public void setContext( ApplicationContext ctx ) {
        this.context = ctx;
    }

    public ApplicationContext getContext() {
        return this.context;
    }

    public void dispose() {
        frame.setVisible( false );
        frame.dispose();
    }

    public void setVisible( boolean b ) {
        frame.setVisible( b );
    }

    public void addModuleComponent( ApplicationModule module ) {
        if( module instanceof VisibleApplicationModule ) {
            primaryModuleDisplay.addTab( module.getName(),
                    ((VisibleApplicationModule)module).getGUI() );
            applicationTabIndex.put( module, primaryModuleDisplay.getSelectedIndex() );
        }
    }

    public void removeModuleComponent( ApplicationModule module ) {
        primaryModuleDisplay.removeTabAt( applicationTabIndex.get( module ) );
    }

    public void addMenuItem( JMenuItem item, String parent ) {
        if( parent == null ) {
            //add directly to the menuBar
            menuBar.add( item );
        } else {
            JMenuItem it = menus.get( parent );
            if( it != null && it instanceof JMenu ) {
                it.add( item );
            }
        }

        if( item instanceof JMenu ) {
            menus.put( ( item ).getText(), item );
        }
    }

    public void removeMenuItem( JMenuItem item ) {
        menuBar.remove( item );
    }

    public String getName() {
        return "appGUI";
    }

    public boolean hasGUI() {
        return false;
    }

    public JComponent getGUI() {
        return null;
    }

    public void execute( String cmd, ArgumentList args ) {
        if( cmd.equals( "" ) ) {
            
        } else if( cmd.equals( "" ) ) {
            
        }
    }

    public void onInsert( ApplicationContext context ) {
        this.setContext( context );
        if( context instanceof DefaultApplicationContext ) {
            ( (DefaultApplicationContext) context ).setApplicationGUI( this );
        }
    }
}
