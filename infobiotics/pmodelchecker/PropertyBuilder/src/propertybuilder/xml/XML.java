
package propertybuilder.xml;

import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathExpressionException;
import org.w3c.dom.Node;

/**
 *
 * @author Ciprian
 */
public interface XML {

    public String lineSep = System.getProperty( "line.separator" );

    public void fromXML( Node source, XPath xp ) throws XPathExpressionException;
    public String toXML();
}
