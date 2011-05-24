

package propertybuilder.pattern;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.regex.Matcher;

/**
 *
 * @author Ciprian
 */
public class SymbolSequence {

    private ArrayList<Symbol> sequence;

    public SymbolSequence() {
        sequence = new ArrayList<Symbol>();
    }

    public void addSymbol( Symbol symbol ) {
        sequence.add( symbol );
    }

    public void deleteSymbol( Symbol symbol ) {
        sequence.remove( symbol );
    }

    public Iterator<Symbol> iterator() {
        return sequence.iterator();
    }

    public int size() {
        return sequence.size();
    }

    public Symbol getSymbolForName( String name ) {
        for( Symbol s : sequence ) {
            if( s.getSymbolName().equals( name ) ) {
                return s;
            }
        }
        return null;
    }

    public Variable getVariable( String varId ) {
        for( Symbol s : sequence ) {
            if( s instanceof Variable ) {
                Variable v = (Variable) s;
                if( v.getId().equals( varId ) ) {
                    return v;
                }
            }
        }

        return null;
    }

    public void parseSequence( String input ) {
        java.util.regex.Pattern p = java.util.regex.Pattern.compile( "#" );
        java.util.regex.Pattern varPattern = java.util.regex.Pattern.compile( "[a-zA-Z0-9_-]+" );
        sequence.clear();
        String[] segments = p.split( input );
        int startIndex = 1;
        if( input.startsWith( "#" ) ) {
            startIndex = 0;
        } else {
            sequence.add( new Literal( segments[0] ) );
        }
        for( int i = startIndex; i < segments.length; i++ ) {
            Matcher m = varPattern.matcher( segments[i] );
            if( m.find() ) {
                String varId = m.group();
                String literalString = segments[i].substring( varId.length() );
                sequence.add( new Variable( varId ) );
                if( !literalString.isEmpty() ) {
                    sequence.add( new Literal( literalString ) );
                }
             }
         }
    }
    
    @Override
    public String toString() {
        StringBuffer buf = new StringBuffer();
        for( Symbol s : sequence ) {
            buf.append( s.getSymbolName() );
        }

        return buf.toString();
    }
}
