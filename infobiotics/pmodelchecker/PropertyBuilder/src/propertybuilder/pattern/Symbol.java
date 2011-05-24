

package propertybuilder.pattern;

/**
 *
 * @author Ciprian
 */
public abstract class Symbol {
    protected SymbolType symbolType;
    protected String symbolName;

    public Symbol( SymbolType symbolType ) {
        setSymbolType( symbolType );
    }

    public void setSymbolType( SymbolType symbolType ) {
        this.symbolType = symbolType;
    }

    public SymbolType getSymbolType() {
        return this.symbolType;
    }

    public void setSymbolName( String symbolName ) {
        this.symbolName = symbolName;
    }

    public String getSymbolName() {
        return this.symbolName;
    }
}
